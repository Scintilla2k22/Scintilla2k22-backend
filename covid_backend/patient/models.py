from django.db import models
from django.db.models.fields import related
from django.db.models.query_utils import select_related_descend 
from user.models import *
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save, post_delete
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
from user.models import *
from django.db.models import Q
from django.conf import settings
from health.models import *
from datetime import datetime 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from health.models import *
from django.utils import timezone
# Create your models here.

User = settings.AUTH_USER_MODEL

class PatientQuerySet(models.QuerySet):         
    """
        Custom get_query_set , based on the lookups provided
    """
    def search(self,query):

        lookup = (
                Q(patient_status__iexact=query) |
                Q(patient_id__iexact = query)|
                Q(name__icontains = query)|
                Q(age__iexact = query)|
                Q(gender__icontains = query)|
                Q(address__icontains = query)|
                Q(covid_facility__icontains = query)|
                Q(created_on__icontains= query)|
                Q(contact_number__iexact=query)
                         
                )

        return self.filter(lookup)


class PatientManager(models.Manager):
    def get_queryset(self):
        return PatientQuerySet(self.model , using = self._db)
     

    def search(self , query = None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)



class PatientProfile(TimeStamped):
    PATIENT_CONDITION = (
        ("1", ("Asymptomataic")),
        ("2", ("Mild")),
        ("3", ("Moderate")),
        ("4", ("severe"))
    )

    GENDER_CHOICE = (
    ("M", ("MALE")),
    ("F", ("FEMALE")),
    ("O", ("OTHERS"))
    )
    
    PATIENT_STATUS = (
        ("A", ("active")),
        ("R", ("recovered")),
        ("M", ("migrated")),
        ('D', ("death")),
        ('H', ("home_isolated"))
    )

    COVID_STATUS = (
        ("S", ("Suspect")),
        ("P", ("Positive")),
        ("N", ("Negative")) 
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    patient_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, null=True, blank=True)
    age  = models.IntegerField(null=True, blank=True)
    admitted_on = models.DateField(auto_now_add=False, auto_now=False, default=timezone.now)
    contact_number = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    patient_status = models.CharField(choices=PATIENT_STATUS, max_length=40, default="A")
    covid_status = models.CharField(choices=COVID_STATUS, max_length=40, default="P")
    remark = models.TextField(blank=True, null=True, default=" ")
    covid_facility = models.TextField(blank=True, null=True, default="G.T.R Base Hospital, Almora")
    health_condition = models.CharField(choices=PATIENT_CONDITION, max_length=30, null=True, blank=True)


    objects = PatientManager()
    class Meta:
        ordering = ['updated_on']
     

    

    def __str__(self):
        return "Patient ID : {0}, name : {1} , status : {2}".format(self.patient_id, self.name, self.get_patient_status_display())



class PatientVaccinationStatus(TimeStamped):
    is_vaccinated = models.BooleanField(blank=True, null=True)   
    patient = models.OneToOneField(PatientProfile,related_name="patient_vaccine_status" ,  on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{0} : {1}".format(self.patient, "vaccinated" if self.is_vaccinated else "not vaccinated")


class Vaccine(TimeStamped):
    VACCINE_TYPE =  ( ("1", ("Covishield")),
                    ("2", ("Covaxin")))
    
    type = models.CharField(choices=VACCINE_TYPE,blank=True,  max_length=266)
    vaccinated_on = models.DateField(auto_now=False,blank=True, auto_now_add=False)
    patient_vaccine = models.ForeignKey(PatientVaccinationStatus, related_name="vaccine_status", on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(PatientProfile, related_name="patient_vaccine", on_delete=models.CASCADE, null=True)
    def __str__(self):
        return "{0} :  {1} | {2}".format(self.patient_vaccine.patient.patient_id, self.get_type_display(), self.vaccinated_on)

class PatientCovidTest(TimeStamped):
    TEST_TYPE = (
        ("1", ("Rapid Antigen")),
        ("2", ("RT-PCR")),
        ("3", ("TrueNat")),
    )

    TEST_RESULT = (
        ("1", ("Positive")),
        ("2", ("Negative")),
        ("3", ("Awaited")),
        ("4", ("Rejected"))
    )
    
    is_tested = models.BooleanField(blank=True, null=True)
    type = models.CharField(choices=TEST_TYPE, null=True, blank=True, max_length=266)
    result = models.CharField(choices=TEST_RESULT, null=True, blank=True,  max_length=266)
    patient = models.OneToOneField(PatientProfile,related_name="patient_covid_test", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{0} | {1} | {2} ".format(self.patient, self.get_type_display(), self.get_result_display())


class PatientMigrate(TimeStamped):
    id = models.AutoField(primary_key=True)
    migrated_to = models.TextField(blank=True, null=False)
    migrated_on = models.DateTimeField(auto_now_add=False, auto_now=False, null=False)
    reason = models.TextField(blank=True, null=False)
    patient = models.OneToOneField(PatientProfile,related_name="patient_migrate",on_delete=models.CASCADE,  unique=True)

    def __str__(self):
        return ("patient : {0} , migrated to : {1} , on {2}".format(self.patient, self.migrated_to, self.migrated_on))



class PatientDeath(TimeStamped):
    expired_on = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    reason = models.TextField(blank=True, null=True)
    patient = models.OneToOneField(PatientProfile,related_name="patient_death", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "patient : {0} | Expired on : {1} | Reason : {2}".format(self.patient.patient_id, self.expired_on, self.reason)



    # def clean(self):
    #     # patient = PatientMigrate.objects.filter(patient=self.patient)

    #     # if patient.exists() and self.id != patient.first().id :
    #     #     raise ValidationError(('Patient is already migrated to {}'.format(patient.first().migrated_to)))

    #     return super().clean()


    # def save(self, *args, **kwargs):
    #     patient = PatientProfile.objects.filter(patient_id=self.patient.patient_id).first()
    #     if patient.patient_status not in ["M", "D"] :
    #         patient.patient_status = 
    #         patient.save()
    #     super(PatientMigrate, self).save(*args, **kwargs)




@receiver(post_save, sender=PatientProfile)
def create_patient_id(sender, instance=None, created=False, **kwargs):
    """
        1. Generate Patient ID
        2. Check whether the migrations model is created or not when patient status changes to migrated
        3. Deallocate bed as soon as the patient  recover , migrate or dead.

    """
    if instance.patient_id is  None:
        date = str(datetime.date(datetime.now())).replace('-', '')
        # print(instance.pk)
        username = int(date)*10000 + instance.id
        instance.patient_id = str(username)
        instance.save() 

    # if instance.patient_status == 'M':
    #     migration = PatientMigrate.objects.filter(patient=instance)
    #     if  migration.count() == 0:
    #         migrate = PatientMigrate(patient=instance, migrated_on=timezone.now())        
    #         migrate.save()   

    if instance.patient_status != 'A':
      
        bed = PatientBed.objects.filter(patient=instance)
        if bed.exists():           
            bed.first().delete()


class BedCount(models.Model):
    total = models.IntegerField(null=True, blank=True, default=0)
    general = models.IntegerField(null=True, blank=True,default=0)
    oxygen = models.IntegerField(null=True, blank=True, default=0)
    icu = models.IntegerField(null=True, blank=True, default=0)
    ventillator = models.IntegerField(null=True, blank=True, default=0)

    def clean(self):
        qs = BedCount.objects.all()
        
        # if self.general + self.oxygen + self.icu + self.ventillator != self.total:
        #     raise ValidationError(('Invalid Entry, Total beds is not properly defined'))
        self.total = self.oxygen + self.ventillator + self.general + self.icu 
        if  qs.count() and qs[0].pk != self.pk :
            raise ValidationError(('Cannot create more than one model, make change on the above one only'))

        return super().clean()


class Bed(models.Model):
    BED_CAT = (
        ("1", ("General Bed")),
        ("2", ("Oxygen Bed")),
        ('3', ("ICU Bed")),
        ('4', ("Ventillator Bed"))
    )

    FLOOR =   ( ("1", ("Floor 1")),
        ("2", ("Floor 2")),
        ('3', ("Floor 3")),
        ('4', ("Floor 4"))
    )

    WARD = ( ("A", ("Ward A")), 
            ( ("B", ("Ward B"))),
            (("OG", ("Obs & Gynae Ward"))),
            (("P", ("Paediatric Ward")))
    )

    bed_number = models.IntegerField(null=True, blank=True)
    bed_id = models.CharField(max_length=266, null=True, blank=True)
    bed_category = models.CharField(choices=BED_CAT, max_length=30, blank=True, null=True)    
    floor = models.CharField(choices=FLOOR, max_length=266, blank=True , null=True)
    ward = models.CharField(choices=WARD, max_length=266, blank=True, null=True)

    class Meta:
        abstract = True


class PatientBed(Bed, TimeStamped):    
    patient = models.OneToOneField(PatientProfile, related_name="patient_bed", on_delete=models.CASCADE,  null=True, blank=True)   
    bed_status = models.BooleanField(default=True)


    def clean(self):
        self.bed_id = "W{0}-F{1}-{2}".format(self.ward ,self.floor,self.bed_number)

        if self.patient.patient_status != "A":
            raise ValidationError(("Bed allotment for {0} patient cannot done".format(self.patient.get_patient_status_display())))

        qs = PatientBed.objects.filter(bed_id=self.bed_id)       

        if  qs.exists()  and  str(self.patient.patient_id) != str(qs.first().patient.patient_id) :
            raise ValidationError(('Bed already alloted'))
        
        if self.bed_status == False:
            raise ValidationError(("Bed can't be alloted with unchecked status."))

        catg_validate = PatientBed.objects.filter(bed_category=self.bed_category)
        bed_count = BedCount.objects.all().first()
        
        if  self.bed_category=="1" and catg_validate.count() >= bed_count.general or \
            self.bed_category=="2" and catg_validate.count() >= bed_count.oxygen or \
                self.bed_category=="3" and catg_validate.count() >= bed_count.icu or \
                    self.bed_category=="4" and catg_validate.count() >= bed_count.ventillator :
            raise ValidationError({"bed_category" : ("Beds are full")})

        return super().clean()


    def __str__(self):
        self.bed_id = "W{0}-F{1}-{2}".format(self.ward ,self.floor,self.bed_number)
        return "{0} ,  Status : {1}".format(self.bed_id, "Taken" if self.bed_status  else "Free")
 


class PatientBedHistory(Bed, TimeStamped):    
    patient = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return "{0} , patient : {1}".format(self.get_bed_category_display(), self.patient)

    def save(self, *args, **kwargs):
        super(PatientBedHistory, self).save(*args, **kwargs)




@receiver(post_save, sender=PatientBed)
def create_patient_bed_history(sender, instance=None, created=False, **kwargs):
    if created:
        PatientBedHistory.objects.create(patient=str(instance.patient_id), bed_number=instance.bed_number, bed_category=instance.bed_category)
    
    if instance.bed_status == False:
        instance.delete()
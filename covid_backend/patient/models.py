from django.db import models 
from user.models import *
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save, post_delete
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
from user.models import *
from django.conf import settings
from health.models import *
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Create your models here.

User = settings.AUTH_USER_MODEL

class PatientProfile(TimeStamped):
    GENDER_CHOICE = (
    ("M", ("MALE")),
    ("F", ("FEMALE")),
    ("O", ("OTHERS"))
    )
    
    PATIENT_STATUS = (
        ("A", ("Active")),
        ("R", ("Recovered")),
        ("M", ("Migrated"))
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    patient_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, null=True, blank=True)
    age  = models.IntegerField(null=True, blank=True)
    contact_number = models.IntegerField(null=True, blank=True)    
    address = models.TextField(null=True, blank=True)
    patient_status = models.CharField(choices=PATIENT_STATUS, max_length=40, default="A")
    covid_facility = models.TextField(blank=True, null=True, default="G.T.R Base Hospital, Almora")
    
    class Meta:
        ordering = ['-pk' , '-created_on', '-updated_on']



    def __str__(self):
        return "Patient ID : {0}, name : {1} , status : {2}".format(self.patient_id, self.name, self.get_patient_status_display())


    # def save(self, *args, **kwargs):
       
    #     super(PatientProfile, self).save(*args, **kwargs)

@receiver(post_save, sender=PatientProfile)
def create_patient_id(sender, instance=None, created=False, **kwargs):
    if instance.patient_id is  None:
        date = str(datetime.date(datetime.now())).replace('-', '')
        # print(instance.pk)
        username = int(date)*10000 + instance.id
        instance.patient_id = str(username)
        instance.save() 

class BedCount(models.Model):
    total = models.IntegerField(null=True, blank=True, default=0)
    general = models.IntegerField(null=True, blank=True,default=0)
    oxygen = models.IntegerField(null=True, blank=True, default=0)
    icu = models.IntegerField(null=True, blank=True, default=0)
    ventillator = models.IntegerField(null=True, blank=True, default=0)

    def clean(self):
        qs = BedCount.objects.all()
        
        if self.general + self.oxygen + self.icu + self.ventillator != self.total:
            raise ValidationError(('Invalid Entry, Total beds is not properly defined'))
            
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
    bed_number = models.IntegerField(null=False, blank=False)
    bed_category = models.CharField(choices=BED_CAT, max_length=30)    

    class Meta:
        abstract = True



class PatientBed(Bed, TimeStamped):    
    patient = models.OneToOneField(PatientProfile, on_delete=models.CASCADE,  unique=True)   
    bed_status = models.BooleanField(default=True)
    def clean(self):
        qs = PatientBed.objects.filter(bed_number=self.bed_number)       

        if  qs.exists() and qs.first().bed_status and  str(self.patient.patient_id) != str(qs.first().patient.patient_id) :
            raise ValidationError(('Bed already alloted'))
        
        if self.bed_status == False:
            raise ValidationError(("Bed can't be alloted with unchecked status."))

        return super().clean()

    def __str__(self):
        return "{0} ,  Status : {1}".format(self.get_bed_category_display(), "Taken" if self.bed_status  else "Free")


    # @property
    # def get_alloted_bed(self):
    #     count = PatientBed.objects.filter(bed_status=True)
    #     return count

class PatientBedHistory(Bed, TimeStamped):    
    patient = models.CharField(max_length=30, null=False, blank=False)

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
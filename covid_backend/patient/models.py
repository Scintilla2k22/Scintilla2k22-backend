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
        print(instance.pk)
        username = int(date)*10000 + instance.id
        instance.patient_id = str(username)
        instance.save() 





class Bed(TimeStamped):
    BED_CAT = (
        ("1", ("General Bed")),
        ("2", ("Oxygen Bed")),
        ('3', ("ICU Bed")),
        ('4', ("Ventillator Bed"))
    )
    bed_number = models.IntegerField(null=False, blank=False)
    bed_category = models.CharField(choices=BED_CAT, max_length=30)
    bed_status = models.BooleanField(default=False)

    def __str__(self):
        return "{0} ,  Status : {1}".format(self.get_bed_category_display(), "Taken" if self.bed_status  else "Free")


class PatientBed(Bed):
    bed_status = True
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} , patient : {1}".format(self.get_bed_category_display(), self.patient.patient_id)


    def save(self, *args, **kwargs):
        
        super(PatientBed, self).save(*args, **kwargs)

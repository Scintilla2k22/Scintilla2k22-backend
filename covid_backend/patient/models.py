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
    
    name = models.CharField(max_length=50, blank=False, null=False)
    icmr = models.CharField(max_length=50, blank=False, null=False, unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, null=True, blank=True)
    age  = models.IntegerField(null=True, blank=True)
    contact_number = models.IntegerField(null=True, blank=True)    
    address = models.TextField(null=True, blank=True)
    patient_status = models.CharField(choices=PATIENT_STATUS, max_length=40, default="A")
    covid_facility = models.TextField(blank=True, null=True, default="G.T.R Base Hospital, Almora")
    


    def __str__(self):
        return "Patient ID : {0}, name : {1} , status : {2}".format(self.icmr, self.name, self.get_patient_status_display())












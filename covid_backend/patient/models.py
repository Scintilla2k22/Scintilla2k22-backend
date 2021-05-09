from django.db import models 
from user.models import *

# Create your models here.


class PatientProfile(TimeStamped):
    GENDER_CHOICE = (
    ("M", ("MALE")),
    ("F", ("FEMALE")),
    ("O", ("OTHERS"))
    )
    icmr = models.CharField(max_length=40, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, null=True, blank=True)
    age  = models.IntegerField(null=False, blank=False)
    contact_1 = models.IntegerField(null=False, blank=False)
    contact_2 = models.IntegerField(null=True, blank=True)
    aadhar_number = models.IntegerField(null=False, blank=False)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Patient : {0}, name : {1}".format(self.icmr, self.name)
from django.db import models 
from user.models import *
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save, post_delete
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
from user.models import *
from django.conf import settings


# Create your models here.

User = settings.AUTH_USER_MODEL

class PatientProfile(TimeStamped):
    GENDER_CHOICE = (
    ("M", ("MALE")),
    ("F", ("FEMALE")),
    ("O", ("OTHERS"))
    )
    
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE )
    icmr = models.CharField(max_length=50, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, null=True, blank=True)
    age  = models.IntegerField(null=True, blank=True)
    contact_1 = models.IntegerField(null=True, blank=True)
    contact_2 = models.IntegerField(null=True, blank=True)
    aadhar_number = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Patient : {0}, name : {1}".format(self.icmr, self.name)




@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance=None, created=False, **kwargs):
    if  instance.is_patient:
        # PatientProfile.objects.create(user=instance)
        print(created, "\n\n\n\n\n")
        if not created:
            patient = PatientProfile( user=instance, icmr=instance.username)
            patient.save()

@receiver(post_delete, sender=PatientProfile)
def delete_user(sender, instance= None, **kwargs):
    user = get_object_or_404(User, username=str(instance.user))
    user.delete()











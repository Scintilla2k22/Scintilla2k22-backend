from django.db import models
# from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save, post_delete
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, blank=False, null=False)   
    is_doctor = models.BooleanField(default=False, blank=False, null=False)
    is_nurse = models.BooleanField(default=False, blank=False, null=False)
    is_patient = models.BooleanField(default=False, blank=False, null=False)
    is_admin = models.BooleanField(default=False, blank=False, null=False)


# User = settings.AUTH_USER_MODEL

class TimeStamped(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class StaffCategory(models.Model):
    STAFF_CATEGORY = (
        ("D", ("DOCTOR")),
        ("N", ("NURSE"))
    )
    title = models.CharField(max_length=30, choices=STAFF_CATEGORY)
    slug = models.SlugField()

    def __str__(self):
        return self.get_title_display()


class MedicalStaffProfile(TimeStamped):
    GENDER_CHOICE = (
        ("M", ("MALE")),
        ("F", ("FEMALE")),
        ("O", ("OTHERS"))
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE )
    staff_category = models.ForeignKey(StaffCategory, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, null=True, blank=True)
    contact_number = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True)


    def __str__(self):
        return "Staff : {0}, ID : {1}".format(self.staff_category, self.user.username)

    # def save(self, *args, **kwargs):
    #     print(self.staff_category)
    #     if self.staff_category is not None and str(self.staff_category) == "NURSE":
    #         print("NURSE")
    #         self.user.is_staff = True 
    #         self.user.save()            
    #     super( MedicalStaffProfile, self).save(*args, **kwargs)



@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance=None, created=False, **kwargs):
    # print(created, "\n\n\n\n\n")
    # staff_query = MedicalStaffProfile.objects.filter(user=instance)
    if instance.is_staff and  created  :
        MedicalStaffProfile.objects.create(user=instance)


@receiver(post_delete, sender=MedicalStaffProfile)
def delete_user(sender, instance= None, **kwargs):
    user = get_object_or_404(CustomUser, username=str(instance.user))
    user.delete()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    from rest_framework.authtoken.models import Token
    if created:
        Token.objects.create(user=instance)
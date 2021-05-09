from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save, post_delete
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token


# Create your models here.
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
        return self.get_staff_category_display()


class MedicalStaffProfile(TimeStamped):
    GENDER_CHOICE = (
        ("M", ("MALE")),
        ("F", ("FEMALE")),
        ("O", ("OTHERS"))
    )

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE, default=1)
    staff_category = models.ForeignKey(StaffCategory, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, null=True, blank=True)
    contact_number = models.IntegerField(blank=False, null=False)
    address = models.TextField(blank=True)


    def __str__(self):
        return "Staff : {0}, ID : {1}".format(self.get_staff_category_display(), self.user.username)



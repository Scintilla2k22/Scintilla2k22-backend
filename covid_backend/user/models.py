from django.db import models
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
    is_admin = models.BooleanField(default=False, blank=False, null=False)
    

    # def save(self, *args, **kwargs):       
    #     permit = (1 if self.is_doctor else 0 ) + (1 if self.is_admin else 0) + (1 if self.is_nurse else 0)
    #     if permit > 1:
    #         raise ValidationError(
    #            message="Permission Denied"
    #         )
    #     print(permit,"permit")
    #     super(CustomUser(), self).save(*args, **kwargs)

    @property
    def get_staff_type(self):
        if self.is_nurse:
            staff = StaffCategory.objects.filter(title="N")
            if staff.exists():
                return staff.first()
            else:
                create_staff = StaffCategory(title="N", slug="NURSE")
                create_staff.save()
                return create_staff
        elif self.is_doctor:
            staff = StaffCategory.objects.filter(title="D")
            if staff.exists():
                return staff.first()
            else:
                create_staff = StaffCategory(title="D", slug="DOCTOR")
                create_staff.save()
                return create_staff
        elif self.is_admin:
            staff = StaffCategory.objects.filter(title="A")
            if staff.exists():
                return staff.first()
            else:
                create_staff = StaffCategory(title="A", slug="ADMIN")
                create_staff.save()
                return create_staff
        return None
         
# User = settings.AUTH_USER_MODEL

class TimeStamped(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class StaffCategory(models.Model):
    STAFF_CATEGORY = (
        ("D", ("DOCTOR")),
        ("N", ("NURSE")),
        ("A", ("ADMIN"))
        
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
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE )
    staff_category = models.ForeignKey(StaffCategory, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, null=True, blank=True)
    contact_number = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True)


    def __str__(self):
        return "Staff : {0}, ID : {1}".format(self.staff_category, self.user.username)

  

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance=None, created=False, **kwargs):
    # print(created, "\n\n\n\n\n")
    # staff_query = MedicalStaffProfile.objects.filter(user=instance)
    if instance.is_staff    :
        if created:
            MedicalStaffProfile.objects.create(user=instance, staff_category=instance.get_staff_type)
        elif not created:
            staff = MedicalStaffProfile.objects.filter(user=instance)
            if staff.exists():
                staff = staff.first()
                staff_type = instance.get_staff_type
                if staff_type is not None:
                    staff.staff_category = staff_type                    
                else:
                    staff.staff_category = None
                staff.save()
            else:
                new_staff = MedicalStaffProfile(user=instance)
                staff_type = instance.get_staff_type
                if staff_type is not None:
                    new_staff.staff_category = staff_type                    
                else:
                    new_staff.staff_category = None
                new_staff.save()    


                
@receiver(post_delete, sender=MedicalStaffProfile)
def delete_user(sender, instance= None, **kwargs):
    user = get_object_or_404(CustomUser, username=str(instance.user))
    user.delete()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    from rest_framework.authtoken.models import Token
    if created:
        Token.objects.create(user=instance)
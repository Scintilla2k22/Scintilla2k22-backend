from django.contrib import admin
from .models import *
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import  TokenProxy
from rest_framework.authtoken.admin import *
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    fieldsets = (

        *UserAdmin.fieldsets, (
            'User type',{
                'fields' : (
                    'is_admin',
                    'is_doctor',
                    'is_nurse',
                    
                ),
                'description': "Select any one of them "
            }
        )
    )


admin.site.register(MedicalStaffProfile)
admin.site.unregister(TokenProxy)
# admin.site.unregister(Token)
# admin.site.register(StaffCategory)
# admin.site.register(CustomUser, CustomUserAdmin)

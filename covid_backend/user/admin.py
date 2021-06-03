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

class MedicalStaffProfileAdmin(admin.ModelAdmin):
    model = MedicalStaffProfile
    list_display = ['user',  'staff_category',  'gender', 'contact_number', 'address']

    # def category(self, obj):
    #     return obj.staff_category.get_title_display() if obj.staff_category.get_title_display() else 'None' 



admin.site.register(MedicalStaffProfile, MedicalStaffProfileAdmin)
admin.site.unregister(TokenProxy)
# admin.site.unregister(Token)
admin.site.register(StaffCategory)
# admin.site.register(CustomUser, CustomUserAdmin)

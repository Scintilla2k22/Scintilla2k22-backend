from django.contrib import admin
from .models import *
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import  TokenProxy
from rest_framework.authtoken.admin import *
from django.contrib import auth
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

@admin.register(MedicalStaffProfile)
class MedicalStaffProfileCustom(admin.ModelAdmin):
    pass
    def has_add_permission(self, request): 
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None): 
        return False
        
admin.site.unregister(TokenProxy)
# admin.site.unregister(Token)
# admin.site.register(StaffCategory)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(auth.models.Group)
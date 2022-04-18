from asyncio import events
from django.contrib import admin
from .models import *
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = Coordinators
    add_form = CustomUserCreationForm
    fieldsets = (

        *UserAdmin.fieldsets, (
            'More Info',{
                'fields' : (
                    'gender',
                    'branch',
                    'year',
                    'contact_number'
                ),
            }
        )
    )



admin.site.register(Events)
admin.site.register(Coordinators, CustomUserAdmin)



from django.contrib import admin
from .models import *
import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib import auth

@admin.register(HealthStatus)
class HealthStatusCustom(admin.ModelAdmin):
    search_fields = ('patient','patient_condition')

    def has_add_permission(self, request): 
        return False
    def has_change_permission(self, request, obj=None):
        return False

admin.site.unregister(auth.models.Group)

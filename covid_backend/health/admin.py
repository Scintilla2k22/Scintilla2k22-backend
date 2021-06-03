from django.contrib import admin
from .models import *

@admin.register(HealthStatus)
class HealthStatusCustom(admin.ModelAdmin):
    search_fields = ('patient','patient_condition')

    def has_add_permission(self, request): 
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None): 
        return False

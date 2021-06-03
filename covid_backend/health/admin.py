from django.contrib import admin
from django.contrib.admin.options import TabularInline
from .models import *

class HealthStatusInline(admin.TabularInline):
    model = HealthStatus


# @admin.register(HealthStatus)
# class HealthStatusCustom(admin.ModelAdmin):
#     search_fields = ('patient','patient_condition')

#     def has_add_permission(self, request): 
#         return False
#     def has_change_permission(self, request, obj=None):
#         return False

# admin.site.unregister(auth.models.Group)
# admin.site.unregister(HealthStatus)

from django.contrib import admin
from .models import *
# Register your models here.


"""

https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin

"""
class PatientBedInline(admin.TabularInline):
    model = PatientBed
    readonly_fields = ['bed_id']


class VaccineInline(admin.TabularInline):
    model = Vaccine

class PatientVaccinationStatusAdmin(admin.ModelAdmin):
    model = PatientVaccinationStatus
    inlines = [VaccineInline ]

class PatientVaccinationStatusInline(admin.StackedInline):
    model = PatientVaccinationStatus

class PatientMigrateInline(admin.StackedInline):
    model = PatientMigrate

class PatientCovidTestInline(admin.TabularInline):
    model = PatientCovidTest

class PatientProfileAdmin(admin.ModelAdmin):
    inlines = [
        PatientBedInline, PatientMigrateInline, PatientCovidTestInline, PatientVaccinationStatusInline
    ]
    list_display = ('name', 'patient_id', 'contact_number', 'address', 'patient_status')
    list_filter = ( 'patient_status' ,'covid_status' , 'health_condition')
    search_fields = ('name', 'patient_id', 'contact_number', 'address', 'patient_status') 
    readonly_fields = ['patient_id']



admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(PatientBedHistory)
admin.site.register(PatientBed)
admin.site.register(BedCount)
admin.site.register(PatientMigrate)
admin.site.register(PatientCovidTest)
admin.site.register(PatientVaccinationStatus , PatientVaccinationStatusAdmin)
admin.site.register(Vaccine)
admin.site.register(PatientDeath)

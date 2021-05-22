from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(PatientProfile)
admin.site.register(PatientBedHistory)
admin.site.register(PatientBed)
admin.site.register(BedCount)
admin.site.register(PatientMigrate)
admin.site.register(PatientCovidTest)
admin.site.register(PatientVaccinationStatus)
admin.site.register(Vaccine)
 
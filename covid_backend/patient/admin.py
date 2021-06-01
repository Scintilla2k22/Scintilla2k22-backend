from django.contrib import admin
from django.utils.functional import empty
from .models import *
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from .resources import *
from django.utils import timezone
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

class PatientDeathInline(admin.StackedInline):
    model = PatientDeath

class PatientCovidTestInline(admin.TabularInline):
    model = PatientCovidTest





# class InputFilter(admin.SimpleListFilter):
#     template = 'patient/input_filter.html'

#     def lookups(self, request, model_admin):
#         # Dummy, required to show the filter.
#         return ((),)

#     def choices(self, changelist):
#         # Grab only the "all" option.
#         all_choice = next(super().choices(changelist))
#         all_choice['query_parts'] = (
#             (k, v)
#             for k, v in changelist.get_filters_params().items()
#             if k != self.parameter_name
#         )
#         yield all_choice

class PatientProfilePastDataFilter(admin.SimpleListFilter):
    parameter_name = 'from'
    # parameter_name_2 = 'to'
    title = _('Past Record')
    template = 'patient/input_filter.html'

    def lookups(self, request, model_admin):
    # Dummy, required to show the filter.
        return (("from", (" from date : ")),)

    def queryset(self, request, queryset):
        global from_, to_
        # print(self.value(), request.GET.get("to", False))
        if self.value() is not None:
            from_ = request.GET.get("from")
            to_ = request.GET.get("to")
            # print("hello", request.GET.get("from", False))
            return queryset.filter(admitted_on__gte=request.GET.get("from"))
        


class PatientProfileCustomFilter(admin.SimpleListFilter):
    title = _('Patient Status')
    parameter_name = 'patient'

    def lookups(self, request, model_admin):
        PatientProfileAdmin.list_display  = ('name', 'patient_id', 'contact_number', 'address', 'patient_status', 'patient_bed_id','is_tested','test_type', 'is_vaccinated', 'vaccine_status')

        
    
        return (
            ("A", _('ACTIVE')),
            ('M', _('MIGRATED')),
            ("D", _("DECEASED")),
            ("R", _("RECOVERED")),
            ('H', _("HOME ISOLATED")),
            
        )

    def queryset(self, request, queryset):
    
        if self.value() is not None:

            if self.value() == "M":
                PatientProfileAdmin.list_display = ('name', 'patient_id', 'contact_number', 'address', 'admitted_on', 'patient_status','is_tested','test_type', 'is_vaccinated', 'vaccine_status', 'patient_migrate_to', 'patient_migrate_on', 'patient_migration_reason')
                PatientProfileAdmin.resource_class = PatientProfileMigrateResource
            elif self.value() == "D":
                PatientProfileAdmin.list_display = ('name', 'patient_id', 'contact_number', 'address', 'admitted_on', 'patient_status', 'is_tested','test_type', 'is_vaccinated', 'vaccine_status', 'patient_expired_on', 'patient_death_cause')
                PatientProfileAdmin.resource_class = PatientProfileDeathResource
            
            elif self.value() == "R" or self.value() == "H":
                PatientProfileAdmin.list_display = ('name', 'patient_id', 'contact_number', 'address', 'admitted_on',  'patient_status' ,'is_tested','test_type', 'is_vaccinated', 'vaccine_status')
                PatientProfileAdmin.resource_class = PatientProfileIsolate
            else:
                PatientProfileAdmin.list_display = ('name', 'patient_id', 'contact_number', 'address', 'admitted_on', 'patient_status', 'patient_bed_id','is_tested','test_type', 'is_vaccinated', 'vaccine_status')
                PatientProfileAdmin.resource_class = PatientProfileResource

            patient_categ = ['A','M', 'D', 'R', 'H' ]
            if self.value() in patient_categ:
                return queryset.filter(patient_status__iexact=self.value())



class PatientProfileAdmin(ImportExportModelAdmin):
    inlines = [
        PatientBedInline, PatientMigrateInline,PatientDeathInline, PatientCovidTestInline, PatientVaccinationStatusInline
    ]
    global LIST_DISPLAY
    # list_display = LIST_DISPLAY
    
    resource_class = PatientProfileResource
    list_filter = ( 'covid_status' , 'health_condition', PatientProfileCustomFilter, PatientProfilePastDataFilter )
    list_display = ('name', 'patient_id', 'contact_number', 'address','admitted_on', 'patient_status', 'patient_bed_id','is_tested','test_type', 'is_vaccinated', 'vaccine_status')
    search_fields = ('name', 'patient_id', 'contact_number', 'address', 'patient_status') 
    readonly_fields = ['patient_id']


    def patient_bed_id(self, obj):
        return obj.patient_bed.bed_id

    def patient_migrate_to(self, obj):
        return obj.patient_migrate.migrated_to
    

    def patient_migrate_on(self, obj):
        return obj.patient_migrate.migrated_on

    def patient_migration_reason(self, obj):
        return obj.patient_migrate.reason

    def patient_expired_on(self, obj):
        return obj.patient_death.expired_on
    
    def patient_death_cause(self, obj):
        return obj.patient_death.reason

    def is_tested(self, obj):
        return obj.patient_covid_test.is_tested
    
    def test_type(self, obj):
        return obj.patient_covid_test.get_type_display()

    def test_result(self, obj):
        return obj.patient_covid_test.result
    
    
    def is_vaccinated(self, obj):
        return obj.patient_vaccine_status.is_vaccinated

    def vaccine_status(self, obj):
        if PatientVaccinationStatus.objects.filter(patient=obj).count() :
            vaccine = Vaccine.objects.filter(patient_vaccine = obj.patient_vaccine_status).last()
            if vaccine:
                return "{0} ( {1})".format( vaccine.get_type_display(), vaccine.vaccinated_on)
        return "NA"

    # def patient_migrate

admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(PatientBedHistory)
admin.site.register(PatientBed)
admin.site.register(BedCount)
admin.site.register(PatientMigrate)
admin.site.register(PatientCovidTest)
admin.site.register(PatientVaccinationStatus , PatientVaccinationStatusAdmin)
admin.site.register(Vaccine)
admin.site.register(PatientDeath)

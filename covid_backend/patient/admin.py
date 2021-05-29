from django.contrib import admin
from django.utils.functional import empty
from .models import *
from django.utils.translation import gettext_lazy as _
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

# Register your models here.


"""
    https://django-import-export.readthedocs.io/en/latest/getting_started.html#exporting
"""

class PatientProfileResource(resources.ModelResource):
    # list_display = ('name', 'patient_id', 'contact_number', 'address', 'patient_status', 'patient_bed_id','is_tested','test_type', 'is_vaccinated', 'vaccine_status')


    # Patient Covid Test record
    is_tested = fields.Field(
        column_name = 'Is Tested',
        attribute='patient_covid_test',
        widget = ForeignKeyWidget(PatientCovidTest, 'is_tested')
    )
    test_type = fields.Field(
        column_name = 'Test Type',
        attribute='patient_covid_test',
        widget = ForeignKeyWidget(PatientCovidTest, 'type'
        )
    )

    # ..............................................


    # Patient Vaccination Status 
    is_vaccinated = fields.Field(
        column_name = 'Is Vaccinated',
        attribute='patient_vaccine_status',
        widget = ForeignKeyWidget(PatientVaccinationStatus, 'is_vaccinated'
        )
    )

    vaccine_status = fields.Field(column_name = 'Vaccine Status')


    # ..............................

    # Patient Migration Details ................

    patient_migrate_to = fields.Field( column_name = "Migrated To")
    patient_migrate_on = fields.Field(column_name = "Migrated On")
    patient_migration_reason = fields.Field(column_name = "Migration Reason")

    def dehydrate_patient_migrate_to(self, obj):
        if PatientMigrate.objects.filter(patient=obj).count():
            return obj.patient_migrate.migrated_to
        return "NA"

    def dehydrate_patient_migrate_on(self, obj):
        if PatientMigrate.objects.filter(patient=obj).count():
            return obj.patient_migrate.migrated_on
        return "NA"

    def dehydrate_patient_migration_reason(self, obj):
        if PatientMigrate.objects.filter(patient=obj).count():
            return obj.patient_migrate.reason
        return "NA"
    #..................................



    # Patient Death Details ................

    patient_expired_on = fields.Field(column_name = "Expired On")
    patient_death_cause = fields.Field(column_name = "Cause Of Death")


    def dehydrate_patient_expired_on(self, obj):
        if PatientDeath.objects.filter(patient=obj):
            return obj.patient_death.expired_on
        return "NA"

    def dehydrate_patient_death_cause(self, obj):
        if PatientDeath.objects.filter(patient=obj):
            return obj.patient_death.reason
        return "NA"
    #.........................


    bed_id = fields.Field(
        column_name='bed_id',
        attribute='patient_bed',
        widget=ForeignKeyWidget(PatientBed, 'bed_id'))
    
    def dehydrate_vaccine_status(self, obj):
        if PatientVaccinationStatus.objects.filter(patient=obj).count() :
            vaccine = Vaccine.objects.filter(patient_vaccine = obj.patient_vaccine_status).last()
            if vaccine:
                return "{0} ( {1})".format( vaccine.get_type_display(), vaccine.vaccinated_on)
        return "NA"



    class Meta:
        model = PatientProfile
        fields = ('name', 'patient_id', 'contact_number', 'created_on',  'address', 'patient_status', 'bed_id', \
            'is_tested','test_type', 'is_vaccinated', 'vaccine_status','patient_migrate_to', 'patient_migrate_on', \
                  'patient_migration_reason' )
        export_order = ('name', 'patient_id','created_on',  'contact_number', 'address', 'patient_status', 'bed_id','is_tested','test_type', 'is_vaccinated', 'vaccine_status')
        exclude = ('patient_migrate_to')


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




class PatientProfileCustomFilter(admin.SimpleListFilter):
    title = _('Patient Status')
    parameter_name = 'patient'

    def lookups(self, request, model_admin):
        PatientProfileAdmin.list_display  = ('name', 'patient_id', 'contact_number', 'address', 'patient_status', 'patient_bed_id','is_tested','test_type', 'is_vaccinated', 'vaccine_status')

        # print(request.GET["patient"])
    
        return (
            ("A", _('ACTIVE')),
            ('M', _('MIGRATED')),
            ("D", _("DECEASED")),
            ("R", _("RECOVERED"))
        )

    def queryset(self, request, queryset):
        print("yes ")

        if self.value() == "M":
            PatientProfileAdmin.list_display = ('name', 'patient_id', 'contact_number', 'address', 'patient_status','is_tested','test_type', 'is_vaccinated', 'vaccine_status', 'patient_migrate_to', 'patient_migrate_on', 'patient_migration_reason')
            print(PatientProfileResource.Meta.fields)
            PatientProfileResource.Meta.exclude = ('patient_bed', "patient_expired_on", 'patient_death_cause')
        elif self.value() == "D":
            PatientProfileAdmin.list_display = ('name', 'patient_id', 'contact_number', 'address', 'patient_status', 'is_tested','test_type', 'is_vaccinated', 'vaccine_status', 'patient_expired_on', 'patient_death_cause')
            PatientProfileResource.Meta.exclude = ('patient_bed', 'patient_migrate_to', 'patient_migrate_on', 'patient_migration_reason')
        elif self.value() == "R" or self.value() == "H":
            PatientProfileAdmin.list_display = ('name', 'patient_id', 'contact_number', 'address', 'patient_status' ,'is_tested','test_type', 'is_vaccinated', 'vaccine_status')
        else:
            PatientProfileAdmin.list_display = ('name', 'patient_id', 'contact_number', 'address', 'patient_status', 'patient_bed_id','is_tested','test_type', 'is_vaccinated', 'vaccine_status')

        patient_categ = ['A','M', 'D', 'R' ]
        if self.value() in patient_categ:
            return queryset.filter(patient_status__iexact=self.value())



class PatientProfileAdmin(ImportExportModelAdmin):
    inlines = [
        PatientBedInline, PatientMigrateInline, PatientCovidTestInline, PatientVaccinationStatusInline
    ]
    global LIST_DISPLAY
    # list_display = LIST_DISPLAY
    resource_class = PatientProfileResource
    list_filter = ( 'covid_status' , 'health_condition', PatientProfileCustomFilter)
    list_display = ('name', 'patient_id', 'contact_number', 'address', 'patient_status', 'patient_bed_id','is_tested','test_type', 'is_vaccinated', 'vaccine_status')
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
        return obj.patient_covid_test.type

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

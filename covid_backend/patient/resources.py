from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from .models import *


"""
    https://django-import-export.readthedocs.io/en/latest/getting_started.html#exporting
"""

class Resource(resources.ModelResource):   


    patient_status = fields.Field(
        column_name = "Patient Status"    )

  
    def dehydrate_patient_status(self, obj):
        return obj.get_patient_status_display()

    health_condition = fields.Field(
        column_name = "Health Condition"
    )

    def dehydrate_health_condition(self, obj):
        return obj.get_health_condition_display()

    
    created_on = fields.Field(
        column_name = "Admitted On",
        attribute = 'created_on'
    )

    # Patient Covid Test record
    is_tested = fields.Field(
        column_name = 'Is Tested',
        attribute='patient_covid_test',
        widget = ForeignKeyWidget(PatientCovidTest, 'is_tested')        
    )
    test_type = fields.Field(
        column_name = 'Test Type',       
    )

    def dehydrate_test_type(self, obj):
        return obj.patient_covid_test.get_type_display()


    
    # ..............................................

    # Patient Vaccination Status 
    is_vaccinated = fields.Field(
        column_name = 'Is Vaccinated',
        attribute='patient_vaccine_status',
        widget = ForeignKeyWidget(PatientVaccinationStatus, 'is_vaccinated'        
        )     )

    vaccine_status = fields.Field(column_name = 'Vaccine Status')
      
    def dehydrate_vaccine_status(self, obj):
        if PatientVaccinationStatus.objects.filter(patient=obj).count() :
            vaccine = Vaccine.objects.filter(patient_vaccine = obj.patient_vaccine_status).last()
            if vaccine:
                return "{0} ( {1})".format( vaccine.get_type_display(), vaccine.vaccinated_on)
        return "NA"

    # ..............................

    class Meta:
        model = PatientProfile
        fields = ['name', 'patient_id', 'contact_number', 'created_on', 'age', 'gender',  'health_condition', 'address', 'patient_status',   'is_tested','test_type', 'is_vaccinated', 'vaccine_status', 'remark']
        abstract = True



class PatientProfileResource(Resource):    
    bed_id = fields.Field(
        column_name='bed_id',
        attribute='patient_bed',
        widget=ForeignKeyWidget(PatientBed, 'bed_id'))
    
    
    class Meta:
        model = PatientProfile
        fields = Resource.Meta.fields + ["bed_id"]
        export_order = ('name', 'patient_id', 'contact_number', 'created_on', 'age', 'gender',  'health_condition', 'address', 'patient_status', 'bed_id', \
            'is_tested','test_type', 'is_vaccinated', 'vaccine_status', 'remark' )



class PatientProfileDeathResource(Resource):

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
    
    class Meta:
        model = PatientProfile
        fields = Resource.Meta.fields + ['patient_status', 'patient_expired_on', 'patient_death_cause']
        export_order = Resource.Meta.fields + ['patient_status', 'patient_expired_on', 'patient_death_cause']

class PatientProfileIsolate(Resource):
    class Meta:
        model = PatientProfile
        fields = export_order = Resource.Meta.fields
        


class PatientProfileMigrateResource(Resource):
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

      
    class Meta:
        model = PatientProfile
        fields = Resource.Meta.fields + ['patient_migrate_to', 'patient_migrate_on', 'patient_migration_reason']
        export_order =Resource.Meta.fields + ['patient_migrate_to', 'patient_migrate_on', 'patient_migration_reason']
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import fields
from rest_framework.fields import NOT_READ_ONLY_WRITE_ONLY
from .models import *
from django.conf import settings
from django.utils import timezone
from health.models import *
from health.serializers import *
User = settings.AUTH_USER_MODEL


# class PatientAdmissionSerializers(serializers.ModelSerializer):
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
#     class Meta:
#         model = CustomUser
#         fields = ("username", "password","password2")

#     def save(self):
#         user = CustomUser(
#             username = self.validated_data["username"], is_patient=True
#         )
#         password = self.validated_data['password']
#         password2 = self.validated_data["password2"]

#         if password != password2:
#             raise serializers.ValidationError({'password': 'Password Fields are not same.'})

#         if CustomUser.objects.filter(username=self.validated_data["username"]).exists():
#             raise serializers.ValidationError({'username': 'Patient with this ICMR ID already admitted '})
        
#         user.set_password(password)
#         user.save()
#         return user



"""
    Nested Relationships in Serializers

    http://www.django-rest-framework.org/api-guide/relations/#nested-relationships

    http://www.django-rest-framework.org/api-guide/relations/#serializer-relations

"""



class PatientBedSerializers(serializers.ModelSerializer):
    patient_id = serializers.CharField( )
    # name = serializers.CharField()
    class Meta:
        model = PatientBed
        fields = ('patient_id', 'bed_number', 'bed_category', 'ward', 'floor')    

    def validate(self, attr):
        bed_id = "W{0}-F{1}-{2}".format(attr["ward"], attr["floor"], attr["bed_number"])

        qs = PatientBed.objects.filter(bed_id=bed_id)  
        if qs.exists() and qs.first().bed_status:
            raise serializers.ValidationError({"bed_number" : ["Bed already alloted"]})

        tbed = BedCount.objects.all()
        if tbed.count() < 1 :
            raise serializers.ValidationError({"bed_number" : ["Invalid Bed number"]})

        catg_validate = PatientBed.objects.filter(bed_category=attr["bed_category"])
        bed_count = tbed.first()
        
        if  attr["bed_category"]=="1" and catg_validate.count() >= bed_count.general or \
            attr["bed_category"]=="2" and catg_validate.count() >= bed_count.oxygen or \
                attr["bed_category"]=="3" and catg_validate.count() >= bed_count.icu or \
                    attr["bed_category"]=="4" and catg_validate.count() >= bed_count.ventillator :
            raise serializers.ValidationError({"bed_category" : ("Beds are full")})

        return attr

    def save(self):       
        patient = get_object_or_404(PatientProfile, patient_id = self.validated_data["patient_id"] )       
        pre_bed = PatientBed.objects.filter(patient = patient)
        if pre_bed.exists():
            pre_bed.first().delete()
        patient_bed = PatientBed(patient = patient)
        bed_history = PatientBedHistory(patient=patient)
        patient_bed.bed_category = bed_history.bed_category = self.validated_data["bed_category"]
        patient_bed.bed_number = bed_history.bed_number = self.validated_data["bed_number"]
        patient_bed.ward = bed_history.ward = self.validated_data["ward"]
        patient_bed.floor = bed_history.floor = self.validated_data["floor"]
        patient_bed.bed_id = bed_history.bed_id = "W{0}-F{1}-{2}".format(self.validated_data["ward"], self.validated_data["floor"], self.validated_data["bed_number"])
        patient_bed.bed_status = bed_history.bed_status = True
        patient_bed.save()
        bed_history.save()
        return PatientBed

class PatientProfileBedSerializers(serializers.ModelSerializer):
    class Meta:
        model = PatientBed
        fields = "__all__"


class PatientMigrateSerializers(serializers.ModelSerializer):
    
    # patient = serializers.CharField(write_only=True, read_only=False, required=True) 
    patient_id = serializers.CharField()
    migrated_on = serializers.DateTimeField(read_only=True)  
    class Meta:
        model = PatientMigrate          
        fields = ('patient_id', 'migrated_on','migrated_to', 'reason')


    def validate(self, attr):
        print(attr["patient_id"])
        patient = get_object_or_404(PatientProfile, patient_id = attr["patient_id"] )

        if PatientMigrate.objects.filter(patient=patient).exists() :
            raise serializers.ValidationError({"patient" : ("Patient is not active")})

        return attr


    def save(self):
        # print(self.validated_data["patient_id"])
        patient = get_object_or_404(PatientProfile, patient_id=self.validated_data["patient_id"])
        migrate = PatientMigrate(patient=patient)
        migrate.migrated_on = timezone.now()
        migrate.migrated_to=self.validated_data["migrated_to"]
        migrate.reason=self.validated_data["reason"]
        patient.patient_status = 'M'          
        migrate.save()      
        patient.save()
               
        return migrate

class PatientDeathSerializers(serializers.ModelSerializer):
    patient_id = serializers.CharField()
    class Meta:
        model = PatientDeath         
        fields = ('patient_id', 'expired_on', 'reason')


    def validate(self, attr):
        print(attr["patient_id"])
        patient = get_object_or_404(PatientProfile, patient_id = attr["patient_id"] )

        if PatientDeath.objects.filter(patient=patient).exists() :
            raise serializers.ValidationError(("Patient is not active"))

        return attr


    def save(self):
        # print(self.validated_data["patient_id"])
        patient = get_object_or_404(PatientProfile, patient_id=self.validated_data["patient_id"])
        death = PatientDeath(patient=patient)
        death.expired_on = self.validated_data["expired_on"]
        death.reason=self.validated_data["reason"]
        patient.patient_status = 'D'
        death.save()
        patient.save()               
        return death



class PatientCovidTestSerializers(serializers.ModelSerializer):
    class Meta:
        model = PatientCovidTest
        fields = "__all__"


class VaccineSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = "__all__"

class PatientVaccinationSerializers(serializers.ModelSerializer):
    vaccine_status = VaccineSerializers(many=True, required=False, allow_null=True)
    class Meta:
        model = PatientVaccinationStatus
        fields = ["is_vaccinated", "vaccine_status"]

class PatientProfileSerializers(serializers.ModelSerializer): 
    patient_id = serializers.CharField(read_only=True, write_only=False)   
    patient_bed = PatientProfileBedSerializers()   
    patient_migrate = PatientMigrateSerializers(read_only=True)
    patient_death = PatientDeathSerializers(read_only=True)
    patient_covid_test = PatientCovidTestSerializers()
    patient_vaccine_status = PatientVaccinationSerializers()
    patient_health_status =  serializers.SerializerMethodField()
    patient_condition = serializers.SerializerMethodField()
    patient_status_display = serializers.SerializerMethodField()
 

    class Meta:
        model = PatientProfile
        fields = ['id','patient_condition', 'patient_id', 'admitted_on', 'updated_on', 'name', 'gender', 'age', 'contact_number', 'address', 'patient_status_display',"patient_status", 'covid_facility','health_condition', 'patient_bed',  'patient_migrate','patient_death',  'covid_status', 'remark', 'patient_covid_test', 'patient_vaccine_status', 'patient_health_status'] 
        # fields = "__all__"
        extra_kwargs = {'patient_status': {'write_only': True}, }
  
    def get_patient_health_status(self, obj):
        hs =  HealthStatus.objects.filter(patient = obj)
        if hs.exists():
            hs = hs.first()
            return hs.get_current_health
        return 0

    def get_patient_status_display(self, obj):
        return obj.get_patient_status_display()

    def get_patient_condition(self, obj):
        hs =  HealthStatus.objects.filter(patient = obj)
        if hs.exists():
            hs = hs.first()
            return hs.get_patient_condition
        return "NA"


    def validate(self, attr):
        
        if attr["patient_bed"] != {}:
            bed_id = "W{0}-F{1}-{2}".format(attr["patient_bed"]["ward"], attr["patient_bed"]["floor"], attr["patient_bed"]["bed_number"])

            qs = PatientBed.objects.filter(bed_id=bed_id)  
            if qs.exists() and qs.first().bed_status:
                raise serializers.ValidationError({"bed_number" : ["Bed already alloted"]})

            tbed = BedCount.objects.all()
            if tbed.count() < 1 :
                raise serializers.ValidationError({"bed_number" : ["Invalid Bed number"]})

            catg_validate = PatientBed.objects.filter(bed_category=attr["patient_bed"]["bed_category"])
            bed_count = tbed.first()
            
            if  attr["patient_bed"]["bed_category"]=="1" and catg_validate.count() >= bed_count.general or \
                attr["patient_bed"]["bed_category"]=="2" and catg_validate.count() >= bed_count.oxygen or \
                    attr["patient_bed"]["bed_category"]=="3" and catg_validate.count() >= bed_count.icu or \
                        attr["patient_bed"]["bed_category"]=="4" and catg_validate.count() >= bed_count.ventillator :
                raise serializers.ValidationError({"bed_category" : ("Beds are full")})

        return attr


    def save(self):            
        patient = PatientProfile(name=self.validated_data["name"])
        # print(self.validated_data)
        patient.age = self.validated_data["age"]
        patient.contact_number = self.validated_data["contact_number"]     
        patient.gender = self.validated_data["gender"]        
        patient.address = self.validated_data["address"]    
        patient.health_condition = self.validated_data["health_condition"]         
        patient.remark = self.validated_data["remark"]      
        patient.patient_status = self.validated_data["patient_status"]
        
        if self.validated_data["patient_covid_test"] and self.validated_data["patient_covid_test"]["is_tested"]:
            if self.validated_data["patient_covid_test"]["result"] == "1":
                patient.covid_status = "P"
            elif self.validated_data["patient_covid_test"]["result"] == "2":
                patient.covid_status = "N"
        else:
            patient.covid_status = "S"

        patient.save()

        # Patient Bed model .......
        pre_bed = PatientBed.objects.filter(patient = patient)
        if pre_bed.exists():
            pre_bed.first().delete()
      
        if self.validated_data["patient_bed"] != {}:
            patient_bed = PatientBed(patient = patient)
            bed_history = PatientBedHistory(patient=patient)
            patient_bed.bed_category = bed_history.bed_category = self.validated_data["patient_bed"]["bed_category"]
            patient_bed.bed_number = bed_history.bed_number = self.validated_data["patient_bed"]["bed_number"]
            patient_bed.ward = bed_history.ward = self.validated_data["patient_bed"]["ward"]
            patient_bed.floor = bed_history.floor = self.validated_data["patient_bed"]["floor"]
            patient_bed.bed_id = bed_history.bed_id = "W{0}-F{1}-{2}".format(self.validated_data["patient_bed"]["ward"], self.validated_data["patient_bed"]["floor"], self.validated_data["patient_bed"]["bed_number"])
            patient_bed.bed_status = bed_history.bed_status = True
            patient_bed.save()
            bed_history.save()   
        # ................................................



        # Patient Covid Test Status ......................
        patient_covid = PatientCovidTest(patient=patient)
        if self.validated_data["patient_covid_test"] != {} and  self.validated_data["patient_covid_test"]["is_tested"]:
            patient_covid.is_tested = self.validated_data["patient_covid_test"]["is_tested"]
            patient_covid.type = self.validated_data["patient_covid_test"]["type"]
            patient_covid.result = self.validated_data["patient_covid_test"]["result"]
        patient_covid.save()     

        # .......................................



        # Patient Vaccination Status.................
        patient_vaccine = PatientVaccinationStatus(patient=patient, is_vaccinated=self.validated_data["patient_vaccine_status"]["is_vaccinated"])
        patient_vaccine.save()
        if self.validated_data["patient_vaccine_status"]["vaccine_status"]:
            for v_stat in self.validated_data["patient_vaccine_status"]["vaccine_status"]:                
                vaccine = Vaccine(patient_vaccine=patient_vaccine)
                vaccine.type = v_stat["type"]
                vaccine.vaccinated_on = v_stat["vaccinated_on"]
                vaccine.save()

        # ..........................................


        return patient

class PatientStatusSerializer(serializers.Serializer):
    PATIENT_STATUS = (
        ("A", ("Active")),
        ("R", ("Recovered")),
        ("M", ("Migrated")),
        ('D', ("Death")),
        ('H', ("Home Isolated"))
    )
 
    patient_status = serializers.ChoiceField(choices=PATIENT_STATUS, required=True)
    patient_bed = PatientProfileBedSerializers()
 
    def validate(self, attr):       
        if attr["patient_status"] == 'A' and (attr["patient_bed"] == {} or attr["patient_bed"] == None):
            raise serializers.ValidationError({"patient_bed" : ("Invalid Entry, please fill bed details")})
            
        if attr["patient_bed"] != {}:
            bed_id = "W{0}-F{1}-{2}".format(attr["patient_bed"]["ward"], attr["patient_bed"]["floor"], attr["patient_bed"]["bed_number"])
            qs = PatientBed.objects.filter(bed_id=bed_id)  

            if qs.exists() :
                raise serializers.ValidationError({"bed_number" : ["Bed already alloted"]})

            tbed = BedCount.objects.all()
            if tbed.count() < 1 :
                raise serializers.ValidationError({"bed_number" : ["Invalid Bed number"]})
         
            catg_validate = PatientBed.objects.filter(bed_category=attr["patient_bed"]["bed_category"])
            bed_count = tbed.first()
            
            if  attr["patient_bed"]["bed_category"]=="1" and catg_validate.count() >= bed_count.general or \
                attr["patient_bed"]["bed_category"]=="2" and catg_validate.count() >= bed_count.oxygen or \
                    attr["patient_bed"]["bed_category"]=="3" and catg_validate.count() >= bed_count.icu or \
                        attr["patient_bed"]["bed_category"]=="4" and catg_validate.count() >= bed_count.ventillator :
                raise serializers.ValidationError({"bed_category" : ("Beds are full")})
          

        return attr
    
    


class PatientProfileCountSerializers(serializers.ModelSerializer): 
    created_count = serializers.IntegerField()
    class Meta:
        model = PatientProfile
        fields = ("created_count",)
        pass
  
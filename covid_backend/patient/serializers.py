from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import fields
from rest_framework.fields import NOT_READ_ONLY_WRITE_ONLY
from .models import *
from django.conf import settings
from django.utils import timezone

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
    patient_id = serializers.CharField()
    # name = serializers.CharField()
    class Meta:
        model = PatientBed
        fields = ('patient_id', 'bed_number', 'bed_category')    

    def save(self):       
        patient = get_object_or_404(PatientProfile, patient_id = self.validated_data["patient_id"] )       
        pre_bed = PatientBed.objects.filter(patient = patient)
        if pre_bed.exists():
            pre_bed.first().delete()
        patient_bed = PatientBed(patient = patient)
        bed_history = PatientBedHistory(patient=patient)
        patient_bed.bed_category = bed_history.bed_category = self.validated_data["bed_category"]
        patient_bed.bed_number = bed_history.bed_number = self.validated_data["bed_number"]
        patient_bed.bed_status = bed_history.bed_status = True
        patient_bed.save()
        bed_history.save()
        return PatientBed

class PatientMigrationSerializer(serializers.ModelSerializer):
    
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
        print(self.validated_data["patient_id"])
        patient = get_object_or_404(PatientProfile, patient_id=self.validated_data["patient_id"])
        migrate = PatientMigrate(patient=patient)
        migrate.migrated_on = timezone.now()
        migrate.migrated_to=self.validated_data["migrated_to"]
        migrate.reason=self.validated_data["reason"]
        patient.covid_facility = self.validated_data["migrated_to"]  
        migrate.save()      
        patient.save()
               
        return migrate



class PatientProfileSerializers(serializers.ModelSerializer): 
    BED_CAT = (
        ("1", ("General Bed")),
        ("2", ("Oxygen Bed")),
        ('3', ("ICU Bed")),
        ('4', ("Ventillator Bed"))
    ) 
    patient_id = serializers.CharField(read_only=True)   
    patient_bed = PatientBedSerializers(read_only=True)   
    patient_migrate = PatientMigrationSerializer(read_only=True)
    bed_number = serializers.IntegerField(write_only=True, read_only=False)
    bed_category = serializers.ChoiceField(choices=BED_CAT,write_only=True, read_only=False)

    class Meta:
        model = PatientProfile
        fields = ['id', 'patient_id', 'created_on', 'updated_on', 'name', 'gender', 'age', 'contact_number', 'address', 'patient_status', 'covid_facility','health_condition', 'patient_bed', "bed_category", "bed_number", "patient_migrate"] 
        # fields = "__all__"
        # extra_kwargs = {'bed_number': {'write_only': True}, 'bed_category' : {"write_only" : True}}

    def validate(self, attr):
        qs = PatientBed.objects.filter(bed_number=attr["bed_number"])  
        if qs.exists() and qs.first().bed_status:
            raise serializers.ValidationError({"bed_number" : ["Bed  already alloted"]})        
        return attr

    def save(self):            
        patient = PatientProfile(name=self.validated_data["name"])
        # print(self.validated_data)
        patient.age = self.validated_data["age"]
        patient.contact_number = self.validated_data["contact_number"]     
        patient.gender = self.validated_data["gender"]        
        patient.address = self.validated_data["address"]    
        patient.health_condition = self.validated_data["health_condition"]        
        patient.save()

        pre_bed = PatientBed.objects.filter(patient = patient)
        if pre_bed.exists():
            pre_bed.first().delete()

        patient_bed = PatientBed(patient = patient)
        bed_history = PatientBedHistory(patient=patient)
        patient_bed.bed_category = bed_history.bed_category = self.validated_data["bed_category"]
        patient_bed.bed_number = bed_history.bed_number = self.validated_data["bed_number"]
        patient_bed.bed_status = bed_history.bed_status = True
        patient_bed.save()
        bed_history.save()   

        return patient

class PatientStatusSerializer(serializers.Serializer):
    PATIENT_STATUS = (
        ("A", ("Active")),
        ("R", ("Recovered")),
        ("M", ("Migrated")),
        ('D', ("Death"))
    )
    model = PatientProfile
    status = serializers.ChoiceField(choices=PATIENT_STATUS, required=True)

 
       

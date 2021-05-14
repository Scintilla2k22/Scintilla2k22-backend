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

class PatientProfileSerializers(serializers.ModelSerializer):  
    patient_id = serializers.CharField(read_only=True)
    bed_number = serializers.CharField(read_only=True)
    class Meta:
        model = PatientProfile
        # fields = ("name", "gender", "age", "contact_number",  "address", "patient_id", "patient_status")
        fields = '__all__'

    def save(self):            
        patient = PatientProfile(name=self.validated_data["name"])            
        # patient.name = self.validated_data["name"]
        patient.age = self.validated_data["age"]
        patient.contact_number = self.validated_data["contact_number"]     
        patient.gender = self.validated_data["gender"]        
        patient.address = self.validated_data["address"]            
        patient.save()  
            
        return patient


class PatientBedSerializers(serializers.ModelSerializer):
    patient_id = serializers.CharField()
    name = serializers.CharField()
    class Meta:
        model = PatientBed
        fields = ('patient_id', 'bed_number', 'bed_category', 'name')    

    def save(self):
        print(self.validated_data["patient_id"])
        patient = get_object_or_404(PatientProfile, patient_id = self.validated_data["patient_id"] )
        self.validated_data["name"] = patient.name
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


class PatientStatusSerializer(serializers.Serializer):
    PATIENT_STATUS = (
        ("A", ("Active")),
        ("R", ("Recovered")),
        ("M", ("Migrated")),
        ('D', ("Death"))
    )
    model = PatientProfile
    status = serializers.ChoiceField(choices=PATIENT_STATUS, required=True)

 
       
class ChangeCovidFacilitySerializer(serializers.Serializer):
    model = PatientProfile
    facility = serializers.CharField(style={'input_type': 'text_area'}, required=True)
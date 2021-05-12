from rest_framework import serializers
from django.shortcuts import get_object_or_404
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
     
    class Meta:
        model = PatientProfile
        fields = ("name", "gender", "age", "contact_number",  "address", "patient_id", "patient_status")

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
    patient_id = serializers.CharField(write_only=True)
    class Meta:
        model = PatientBed
        fields = ('patient_id', 'bed_number', 'bed_category')    

    def save(self):
        patient = get_object_or_404(PatientProfile, patient_id = self.validated_data["patient_id"] )
        pre_bed = PatientBed.objects.filter(patient = patient)
        if pre_bed.exists():
            pre_bed.first().patient = None
            pre_bed.first().bed_status = False
            pre_bed.first().save()
        patient_bed = PatientBed(patient = patient)
        bed_history = PatientBedHistory(patient=patient)
        patient_bed.bed_category = bed_history.bed_category = self.validated_data["bed_category"]
        patient_bed.bed_number = bed_history.bed_number = self.validated_data["bed_number"]
        patient_bed.bed_status = bed_history.bed_status = True
        patient_bed.save()
        bed_history.save()
        return PatientBed
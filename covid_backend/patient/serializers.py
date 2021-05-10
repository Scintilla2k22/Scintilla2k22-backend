from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *
from django.conf import settings

User = settings.AUTH_USER_MODEL


class PatientAdmissionSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ("username", "password","password2")

    def save(self):
        user = CustomUser(
            username = self.validated_data["username"], is_patient=True
        )
        password = self.validated_data['password']
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({'password': 'Password Fields are not same.'})

        if CustomUser.objects.filter(username=self.validated_data["username"]).exists():
            raise serializers.ValidationError({'username': 'Patient with this ICMR ID already admitted '})
        
        user.set_password(password)
        user.save()
        return user

class PatientProfileSerializers(serializers.ModelSerializer):  
    class Meta:
        model = PatientProfile
        fields = ("name", "gender", "age", "contact_1","contact_2","aadhar_number", "address")

    def save(self, request_user):        
        user = get_object_or_404(CustomUser, username=str(request_user))      
        name = self.validated_data["name"]       
        user.first_name = name      
        user.save()
        if PatientProfile.objects.filter(user=user).exists():
            patient = PatientProfile.objects.get(user=user)
        else:
            patient = PatientProfile( user= user)      
        patient.age = self.validated_data["age"]
        patient.contact_1 = self.validated_data["contact_1"]
        patient.contact_2 = self.validated_data["contact_2"]
        patient.gender = self.validated_data["gender"]
        patient.aadhar_number = self.validated_data["aadhar_number"]
        patient.address = self.validated_data["address"]
        patient.save()
        return patient
from django.db.models import fields
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *
from django.conf import settings
from patient.models import *

class PatientHealthUpdateSerializers(serializers.ModelSerializer):  
    username = serializers.CharField(write_only=True)
    class Meta:
        model = HealthStatus
        fields = ("username","patient_condition", "oxy_level", "blood_pres_systolic", "blood_pres_diastolic",  "temperature")

    def save(self):            
        patient = get_object_or_404(PatientProfile, patient_id=self.validated_data["username"])

        health_update = HealthStatus(patient=patient)
        health_update.patient_condition = self.validated_data["patient_condition"]
        health_update.oxy_level = self.validated_data["oxy_level"]
        health_update.blood_pres_systolic = self.validated_data["blood_pres_systolic"]
        health_update.blood_pres_diastolic = self.validated_data["blood_pres_diastolic"]
        health_update.temperature = self.validated_data["temperature"]
        health_update.save()



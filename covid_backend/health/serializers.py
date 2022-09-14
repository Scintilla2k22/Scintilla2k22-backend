from msilib.schema import File
from django.db.models import fields
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *
from django.conf import settings
from .models import *

class PatientHealthUpdateSerializers(serializers.ModelSerializer):  
    username = serializers.CharField(write_only=True)
    patient_condition_display = serializers.SerializerMethodField()
    class Meta:
        model = HealthStatus
        fields = ("username" ,"patient_condition","patient_condition_display", "oxy_level","pulse_rate", "blood_pres_systolic", "blood_pres_diastolic",  "temperature", "created_on", "respiration_rate")

    def get_patient_condition_display(self, obj):
        return obj.get_patient_condition_display()
        
    def save(self):            
        patient = get_object_or_404(PatientProfile, patient_id=self.validated_data["username"])
        patient.health_condition = self.validated_data["patient_condition"]
        health_update = HealthStatus(patient=patient)
        health_update.patient_condition = self.validated_data["patient_condition"]
        health_update.oxy_level = self.validated_data["oxy_level"]
        health_update.blood_pres_systolic = self.validated_data["blood_pres_systolic"]
        health_update.blood_pres_diastolic = self.validated_data["blood_pres_diastolic"]
        health_update.temperature = self.validated_data["temperature"]
        health_update.pulse_rate = self.validated_data["pulse_rate"]
        health_update.respiration_rate = self.validated_data["respiration_rate"]
        health_update.save()
        patient.save()
        
        return health_update
        

class OxyLevelReadingSerializer(serializers.ModelSerializer):
    y = serializers.IntegerField(source = "oxy_level")
    x = serializers.DateTimeField(source = "created_on")
    # patient = serializers.CharField(write_only=True, read_only=False, required=True) 
    class Meta:
        model = HealthStatus    
        fields = ('x','y')

class TemperatureReadingSerializer(serializers.ModelSerializer):
    y = serializers.DecimalField(source = "temperature", max_digits=8, decimal_places=2)
    x = serializers.DateTimeField(source = "created_on")
    
    # patient = serializers.CharField(write_only=True, read_only=False, required=True) 
    class Meta:
        model = HealthStatus
        fields = ('x','y')
  
class PulseRateReadingSerializer(serializers.ModelSerializer):
    y = serializers.IntegerField(source = "pulse_rate")
    x = serializers.DateTimeField(source = "created_on")
    
    # patient = serializers.CharField(write_only=True, read_only=False, required=True) 
    class Meta:
        model = HealthStatus
        fields = ('x','y')

  
class RespiratoryRateReadingSerializer(serializers.ModelSerializer):
    y = serializers.IntegerField(source = "respiration_rate")
    x = serializers.DateTimeField(source = "created_on")
    
    # patient = serializers.CharField(write_only=True, read_only=False, required=True) 
    class Meta:
        model = HealthStatus
        fields = ('x','y')

  
class BPRateReadingSerializer(serializers.ModelSerializer):
    dy = serializers.IntegerField(source = "blood_pres_diastolic")
    sy = serializers.IntegerField(source = "blood_pres_systolic")
    x = serializers.DateTimeField(source = "created_on")
    
    # patient = serializers.CharField(write_only=True, read_only=False, required=True) 
    class Meta:
        model = HealthStatus
        fields = ('x','dy', 'sy')

  
 
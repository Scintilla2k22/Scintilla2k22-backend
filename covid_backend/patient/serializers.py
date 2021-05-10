from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *
from django.conf import settings

User = settings.AUTH_USER_MODEL


class PatientAdmissionSerializers(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = CustomUser
        fields = ("username")

    def save(self):
        user = CustomUser(
            username = self.validated_data["username"], is_staff=False, is_patient=True
        )
        
        if CustomUser.objects.filter(username=self.validated_data["username"]).exists():
            raise serializers.ValidationError({'username': 'Patient with this ICMR ID already admitted '})

        password = "ICMR-"+self.validated_data["username"]
        user.set_password(password)
        user.save()
        return user
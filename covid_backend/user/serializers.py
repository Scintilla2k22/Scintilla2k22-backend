from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *


class MedicalStaffRegistrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ("username", "password", "password2")
        extra_kwargs = {
        'password' : {'write_only': True}
        }

    def save(self):
        user = User(
            username = self.validated_data["username"],
        )
        password = self.validated_data['password']
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({'password': 'Password Fields are not same.'})

        if User.objects.filter(username=self.validated_data["username"]).exists():
            raise serializers.ValidationError({'username': 'Staff member already registered with this ID'})

        user.set_password(password)
        user.save()
        return user
   

class MedicalStaffProfileSerializers(serializers.ModelSerializer):
    STAFF_CATEGORY = (
        ("D", ("DOCTOR")),
        ("N", ("NURSE"))
    )
    first_name = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    last_name = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    email = serializers.EmailField(style={'input_type': 'email'}, write_only=True )
    staff_category = serializers.ChoiceField(choices=STAFF_CATEGORY, write_only=True)

    class Meta:
        model = MedicalStaffProfile
        fields = ("first_name", "last_name","email", "staff_category", "gender", "contact_number", "address")

    def save(self, request_user):
        # print(request_user)
        user = get_object_or_404(User, username=str(request_user))
        email = self.validated_data["email"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        user.first_name = first_name
        user.last_name = last_name
        user_email_validator = User.objects.filter(email=self.validated_data["email"])
        if user_email_validator.exists() and user_email_validator.first().username != str(user) :
            raise serializers.ValidationError({"email": "Email address is already taken."})
        user.email = email
        user.save()
        if MedicalStaffProfile.objects.filter(user=user).exists():
            MedicalStaffProfile = MedicalStaffProfile.objects.get(user=user)
        else:
            MedicalStaffProfile = MedicalStaffProfile( user= user)
        staff_catg_model = get_object_or_404(StaffCategory, slug=self.validated_data["staff_category"])
        MedicalStaffProfile.bio = staff_catg_model
        MedicalStaffProfile.contact_number = self.validated_data["contact_number"]
        MedicalStaffProfile.gender = self.validated_data["gender"]
        MedicalStaffProfile.address = self.validated_data["address"]
        MedicalStaffProfile.save()
        return MedicalStaffProfile
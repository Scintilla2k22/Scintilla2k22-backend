from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *
from .views import *
# from django.conf import settings
# User = settings.AUTH_USER_MODEL


class MedicalStaffRegistrationSerializers(serializers.ModelSerializer):
    STAFF_CATEGORY = (
        ("D", ("DOCTOR")),
        ("N", ("NURSE")),
        ('A', ('Admin'))
    )
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    staff_categ = serializers.ChoiceField(choices=STAFF_CATEGORY, write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "password", "password2", "staff_categ")
        extra_kwargs = {
        'password' : {'write_only': True}
        }

    def save(self):
        user = CustomUser(
            username = self.validated_data["username"], is_staff=True
        )
        password = self.validated_data['password']
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({'password': 'Password Fields are not same.'})

        if CustomUser.objects.filter(username=self.validated_data["username"]).exists():
            raise serializers.ValidationError({'username': 'Staff member already registered with this ID'})

        user.set_password(password)
        user_categ = self.validated_data["staff_categ"]
        user.is_staff = True
        if user_categ == "D":
            user.is_doctor = True
        elif user_categ == "N":
            user.is_nurse = True
        elif user_categ == "A":
            user.is_admin = True
        
        user.save()
        return user
   

class MedicalStaffProfileSerializers(serializers.ModelSerializer):
    STAFF_CATEGORY = (
        ("D", ("DOCTOR")),
        ("N", ("NURSE")),
        ("A", ("ADMIN"))
    )
    first_name = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    last_name = serializers.CharField(style={'input_type': 'text'}, write_only=True)
    email = serializers.EmailField(style={'input_type': 'email'}, write_only=True )
    staff_category = serializers.ChoiceField(choices=STAFF_CATEGORY, write_only=True)

    class Meta:
        model = MedicalStaffProfile
        fields = ("first_name", "last_name","email", "staff_category", "gender", "contact_number", "address")

    def save(self, request_user):
        staff_category_dict = {
        "D" : "DOCTOR",
        "N" : "NURSE",
        "A" : "ADMIN"
        }              
        user = get_object_or_404(CustomUser, username=str(request_user))
        email = self.validated_data["email"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        user.first_name = first_name
        user.last_name = last_name
        user_email_validator = CustomUser.objects.filter(email=self.validated_data["email"])
        
        if user_email_validator.exists() and user_email_validator.first().username != str(user) :
            raise serializers.ValidationError({"email": "Email address is already taken."})
        user.email = email
        user.save()
    
        if MedicalStaffProfile.objects.filter(user=user).exists():
            staff = MedicalStaffProfile.objects.get(user=user)
        else:
            staff = MedicalStaffProfile( user= user)

        # StaffCategory should be created        
        staff_catg_model = get_object_or_404(StaffCategory, slug=staff_category_dict[self.validated_data["staff_category"]])
        staff.staff_category = staff_catg_model
        staff.contact_number = self.validated_data["contact_number"]
        staff.gender = self.validated_data["gender"]
        staff.address = self.validated_data["address"]
        staff.save()
       
        return staff



class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
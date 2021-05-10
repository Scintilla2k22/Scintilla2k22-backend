# third party imports
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.conf import settings
from.models import *

User = settings.AUTH_USER_MODEL


class PatientAdmissionView(APIView):
   
    def post(self, request, *args, **kwargs):        
        
        response = dict()
        serializer = PatientAdmissionSerializers(data=request.data)
        if serializer.is_valid():              
            serializer.save() 
            user = get_object_or_404(CustomUser, username=serializer.validated_data["username"])               
            response["data"] = serializer.data
            token, created = Token.objects.get_or_create(user=user)
            response["data"]["token"] = token.key           
            response["status"] = status.HTTP_201_CREATED
            response["msg"] = "Patient Admitted successfully"
            return Response(response)
        else:
            return Response({"data": serializer.errors, "status":status.HTTP_400_BAD_REQUEST })


class PatientProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, *args, **kwargs):       
            serializer = PatientProfileSerializers(data=request.data)
            
            if serializer.is_valid():
                serializer.save(request.user.username)
                return Response({"data":request.data, "status":status.HTTP_201_CREATED, "msg" : "Patient admission successfully." })
            else:
                return Response({"data": serializer.errors, "status" : status.HTTP_400_BAD_REQUEST })

    def get(self, request, *args, **kwargs):
      
        user = get_object_or_404(CustomUser, username=request.user.username)
        if PatientProfile.objects.filter(user=user).exists():
            patient_profile = PatientProfile.objects.get(user=user)
            serializer = PatientProfileSerializers(patient_profile, many=False)
            data =   {'data': serializer.data, 'status': status.HTTP_200_OK }
            data["data"]["ICMR ID"] = user.username
            data["data"]["name"] = patient_profile.name
            data["data"]["age"] = patient_profile.age
            data["data"]["gender"] = patient_profile.gender
            data["data"]["contact_1"] = patient_profile.contact_1
            data["data"]["contact_2"] = patient_profile.contact_2
            data["data"]["aadhar_number"] = patient_profile.aadhar_number
            data["data"]["address"] = patient_profile.address                         
            return Response(data)
        else:
            return Response({'data': "Patient doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})


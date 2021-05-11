from django.shortcuts import render

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

# Create your views here.


class MedicalStaffRegistrationView(APIView):
   
    def post(self, request, *args, **kwargs):        
        staff_category_dict = {
        "D" : "DOCTOR",
        "N" : "NURSE"
        }
        response = dict()
        serializer = MedicalStaffRegistrationSerializers(data=request.data)
        if serializer.is_valid():              
            serializer.save() 
            user = get_object_or_404(CustomUser, username=serializer.validated_data["username"])               
            response["data"] = serializer.data
            token, created = Token.objects.get_or_create(user=user)
            response["data"]["token"] = token.key
            response["data"]["staff_category"] = staff_category_dict[str(serializer.validated_data["staff_categ"])]
            response["status"] = status.HTTP_201_CREATED
            response["msg"] = "staff member registered successfully"
            return Response(response)
        else:
            return Response({"data": serializer.errors, "status":status.HTTP_400_BAD_REQUEST })




class LoginUserView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = {}
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            profile = MedicalStaffProfile.objects.get(user=user)
            token, created = Token.objects.get_or_create(user=user)
            response['data'] = {}
            response['data']['token'] = token.key        
            response['data']['staff_id'] = user.username       
            if user.is_doctor:
                response['data']['staff_category'] = "DOCTOR"    
            elif user.is_nurse:
                response['data']['staff_category'] = 'NURSE'
            elif user.is_admin:
                response['data']['staff_category'] = 'ADMIN'
            response['status'] = status.HTTP_200_OK
            response['msg'] = "You are Successfully logged in"           
            return Response(response)
        else:
            return Response({"msg":'Invalid staff ID','status':status.HTTP_400_BAD_REQUEST}) 


class LogoutUserView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"status": status.HTTP_200_OK })


class MedicalStaffProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, *args, **kwargs):       
            serializer = MedicalStaffProfileSerializers(data=request.data)
            
            if serializer.is_valid():
                serializer.save(request.user.username)
                return Response({"data":request.data, "status":status.HTTP_201_CREATED, "msg" : "Profile created." })
            else:
                return Response({"data": serializer.errors, "status" : status.HTTP_400_BAD_REQUEST })

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, username=request.user.username)
        if MedicalStaffProfile.objects.filter(user=user).exists():
            user_profile_qs = MedicalStaffProfile.objects.get(user=user)
            serializer = MedicalStaffProfileSerializers(user_profile_qs, many=False)
            data =   {'data': serializer.data, 'status': status.HTTP_200_OK }
            data["data"]["staff id"] = user.username
            data["data"]["email"] = user.email
            data["data"]["name"] = str(user.first_name +" "+ user.last_name)                         
            return Response(data)
        else:
            return Response({'data': "Profile doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})



   
class ChangePasswordView(generics.GenericAPIView):
        serializer_class = ChangePasswordSerializer
        model = CustomUser
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def patch(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():             
                if not self.object.check_password(serializer.data.get("current_password")):
                    return Response({"msg": "Check Your password correctly",'status': status.HTTP_400_BAD_REQUEST,})            
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': status.HTTP_200_OK,
                    'msg': 'Password updated successfully',
                    
                }
                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
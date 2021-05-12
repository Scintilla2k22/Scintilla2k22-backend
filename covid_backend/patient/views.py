# third party imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404 
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes

from.models import *

User = settings.AUTH_USER_MODEL


# class PatientAdmissionView(APIView):
   
#     def post(self, request, *args, **kwargs):        
        
#         response = dict()
#         serializer = PatientAdmissionSerializers(data=request.data)
#         if serializer.is_valid():              
#             serializer.save() 
#             user = get_object_or_404(CustomUser, username=serializer.validated_data["username"])               
#             response["data"] = serializer.data
#             token, created = Token.objects.get_or_create(user=user)
#             response["data"]["token"] = token.key           
#             response["status"] = status.HTTP_201_CREATED
#             response["msg"] = "Patient Admitted successfully"
#             return Response(response)
#         else:
#             return Response({"data": serializer.errors, "status":status.HTTP_400_BAD_REQUEST })


class PatientProfileView(APIView):
   
    def post(self, request, *args, **kwargs):       
            serializer = PatientProfileSerializers(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"data":request.data, "status":status.HTTP_201_CREATED, "msg" : "Patient admission successfully." })
            else:
                return Response({"data": serializer.errors, "status" : status.HTTP_400_BAD_REQUEST })

    def get(self, request, *args, **kwargs):      
        patient_profile = PatientProfile.objects.all()
        serializers = PatientProfileSerializers(patient_profile, many=True)
        data =   {'data': serializers.data, 'status': status.HTTP_200_OK }      
        if patient_profile.exists():                         
            return Response(data)
        else:
            return Response({'data': "Patient doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})


@api_view(['GET'])
def get_patient_profile(request, **kwargs):
    patient = get_object_or_404(PatientProfile,patient_id= kwargs.get('id'))
    if patient:
        serializer = PatientProfileSerializers(patient, many=False)
        data = {'data' : serializer.data, 'status' :status.HTTP_200_OK }
        return Response(data)
    else:
        return Response({'data': "Patient  doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})




@api_view(['POST'])
def bed_allotment(request):
    serializer = PatientBedSerializers( data = request.data)
    qs = PatientBed.objects.filter(bed_number=request.data["bed_number"])  
    if qs.exists() and qs.first().bed_status:
        return Response({"data": "Bed already alloted ", "status" : status.HTTP_400_BAD_REQUEST })
    
    if serializer.is_valid():
        serializer.save()
        return Response({"data": request.data , "status":status.HTTP_201_CREATED, "msg" : "Bed alloted to patient {}".format(request.data["patient_id"]) })
    else:
        return Response({"data": serializer.errors, "status" : status.HTTP_400_BAD_REQUEST })


@api_view(["GET"])
def get_alloted_beds(request):
    total_bed = PatientBed.objects.filter(bed_status=True)
    general_bed = PatientBed.objects.filter(bed_status=True, bed_category="1")
    oxy_bed = PatientBed.objects.filter(bed_status=True, bed_category="2")
    icu_bed = PatientBed.objects.filter(bed_status=True, bed_category="3")
    ventillator_bed = PatientBed.objects.filter(bed_status=True, bed_category="4")
    serializers = PatientBedSerializers(total_bed, many=True)
    bed = { "total" : total_bed.count() , 
            "oxygen" : oxy_bed.count(),
            "icu" : icu_bed.count(),
            "ventillator" : ventillator_bed.count()}

    data = {"data":serializers.data, "bed": bed, "status": status.HTTP_200_OK}
    
    return Response(data)


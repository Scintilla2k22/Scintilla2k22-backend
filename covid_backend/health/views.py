import json
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404 
from rest_framework import generics
from rest_framework.response import Response
from.models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .paginations import *
import pandas as pd

# Create your views here.

class PatientHealthUpdateView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, *args, **kwargs):
        serializer = PatientHealthUpdateSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"data":request.data, "status":status.HTTP_201_CREATED, "msg" : "Patient Health updated ." })
        else:
            return Response({"data": serializer.errors, "status" : status.HTTP_400_BAD_REQUEST })


# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_patients_health(request, **kwargs):
    patient = get_object_or_404(PatientProfile,patient_id = kwargs.get('icmr'))
    health_history = HealthStatus.objects.filter(patient=patient)[:5]
    serializer = PatientHealthUpdateSerializers(health_history, many=True)
    data = {'data' : serializer.data, 'status' :status.HTTP_200_OK }

    if health_history.exists():
        return Response(data)
    else:
        return Response({'data': "Patient Health history doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})


class PatientHealthStatusList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = PatientHealthUpdateSerializers
    pagination_class = PatientHealthStatusListPagination

    def get_queryset(self):
        patient = get_object_or_404(PatientProfile,patient_id = self.kwargs['icmr'])
        health_history = HealthStatus.objects.all().filter(patient=patient)
        return health_history


@api_view(['GET'])
def get_patients_oxy_level(request, **kwargs):
    patient = get_object_or_404(PatientProfile,patient_id = kwargs.get('icmr'))
    health_history = HealthStatus.objects.filter(patient=patient)[:5]
    serializer = OxyLevelReadingSerializer(health_history, many=True)
    data = {'data' : serializer.data, 'status' :status.HTTP_200_OK }

    if health_history.exists():
        return Response(data)
    else:
        return Response({'data': "Patient Health history doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})


@api_view(['GET'])
def get_patients_temperature_level(request, **kwargs):
    patient = get_object_or_404(PatientProfile,patient_id = kwargs.get('icmr'))
    health_history = HealthStatus.objects.filter(patient=patient)[:5]
    serializer = TemperatureReadingSerializer(health_history, many=True)
    data = {'data' : serializer.data, 'status' :status.HTTP_200_OK }

    if health_history.exists():
        return Response(data)
    else:
        return Response({'data': "Patient Health history doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})

@api_view(['GET'])
def get_patients_respiratory_rate(request, **kwargs):
    patient = get_object_or_404(PatientProfile,patient_id = kwargs.get('icmr'))
    health_history = HealthStatus.objects.filter(patient=patient)[:5]
    serializer = RespiratoryRateReadingSerializer(health_history, many=True)
    data = {'data' : serializer.data, 'status' :status.HTTP_200_OK }

    if health_history.exists():
        return Response(data)
    else:
        return Response({'data': "Patient Health history doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})

@api_view(['GET'])
def get_patients_bp_level(request, **kwargs):
    patient = get_object_or_404(PatientProfile,patient_id = kwargs.get('icmr'))
    health_history = HealthStatus.objects.filter(patient=patient)[:5]
    serializer = BPRateReadingSerializer(health_history, many=True)
    data = {'data' : serializer.data, 'status' :status.HTTP_200_OK }

    if health_history.exists():
        return Response(data)
    else:
        return Response({'data': "Patient Health history doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})

@api_view(['GET'])
def get_patients_pulse_rate(request, **kwargs):
    patient = get_object_or_404(PatientProfile,patient_id = kwargs.get('icmr'))
    health_history = HealthStatus.objects.filter(patient=patient)[:5]
    serializer = PulseRateReadingSerializer(health_history, many=True)
    data = {'data' : serializer.data, 'status' :status.HTTP_200_OK }

    if health_history.exists():
        return Response(data)
    else:
        return Response({'data': "Patient Health history doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})

@api_view(['GET'])
def get_patients_readings(request, **kwargs):
    patient = get_object_or_404(PatientProfile,patient_id = kwargs.get('icmr'))
    health_history = HealthStatus.objects.filter(patient=patient)[:5]
    temp_serializer = TemperatureReadingSerializer(health_history, many=True)
    resp_serializer = RespiratoryRateReadingSerializer(health_history, many=True)
    bp_serializer = BPRateReadingSerializer(health_history, many=True)
    pulse_serializer = PulseRateReadingSerializer(health_history, many=True)
    oxy_serializer = OxyLevelReadingSerializer(health_history, many=True)
    df = pd.DataFrame(bp_serializer.data)
    bpd_df = df[["x", "dy"]]
    bps_df  =  df[["x", "sy"]]
    bpd_df.rename(columns = {'dy':'y'},inplace=True)
    bps_df.rename(columns = {'sy':'y'},inplace=True)
    
    bp_serializer = {
        "systolic" : bps_df.to_dict("records") ,
        "diastolic" : bpd_df.to_dict("records") 
    }
    print("bp_serializer \n\n\n\n\n\n\n", bp_serializer)
    serializer = {
        "temperature": temp_serializer.data,
        "respiratory": resp_serializer.data,
        "bp": bp_serializer,
        "pulse": pulse_serializer.data,
        "oxy": oxy_serializer.data

    }
    data = {'data' : serializer, 'status' :status.HTTP_200_OK }

    if health_history.exists():
        return Response(data)
    else:
        return Response({'data': "Patient Health history doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})


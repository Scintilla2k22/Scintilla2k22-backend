# third party imports
from health.models import HealthStatus
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404 
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from.models import *
from django.utils.timezone import datetime
from .paginations import *
from django.db.models.functions import TruncDay
from django.db.models import Count

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
    permission_classes = [IsAuthenticated,]
    def post(self, request, *args, **kwargs):       
            serializer = PatientProfileSerializers(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"data":request.data, "status":status.HTTP_201_CREATED, "msg" : "Patient admission successfully." })
            else:
                return Response({"data": serializer.errors, "status" : status.HTTP_400_BAD_REQUEST })

    def get(self, request, *args, **kwargs):      
        # patient_profile = PatientProfile.objects.filter(patient_status="A").exclude( healthstatus__created_on__gte = datetime.date(datetime.now()))
        patient_profile = PatientProfile.objects.all().filter(patient_status='A')
        # unchecked = patient_profile.count()
        # total = PatientProfile.objects.all().count()
        serializers = PatientProfileSerializers(patient_profile, many=True)
        data =   {'data': serializers.data, 'status': status.HTTP_200_OK }      
        if patient_profile.exists():                         
            return Response(data)
        else:
            return Response({'data': "Patient doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})


 
class PatientsList(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = PatientProfileSerializers
    pagination_class = PatientListPagination

    def get_queryset(self):
        query = self.kwargs.get('id',False) if not self.kwargs.get('id',False) else 'A'
        queryset = PatientProfile.objects.all().filter(patient_status=query)
        return queryset



@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_searched_patients(request, **kwargs):
    query = kwargs.get("query").lower()
    status_list = ("active", "migrated", "death", "recovered", "home_isolated")
    status_dict = {"active" : "A", "migrated" : "M", "death" : "D", "recovered" : "R", "home_isolated" : "H"}

    if query in status_list:
        qs  = PatientProfile.objects.filter(patient_status=status_dict[query])
    else:
        qs = PatientProfile.objects.search(query=kwargs.get("query"))
    serializer = PatientProfileSerializers(qs, many=True)
    if qs.exists():        
        return Response({"data": serializer.data, "status": status.HTTP_200_OK })
    else:
        return Response({'data': "Searched result not found :-( ", 'status': status.HTTP_404_NOT_FOUND})

 

# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_patient_profile(request, **kwargs):
    patient = get_object_or_404(PatientProfile,patient_id= kwargs.get('id'), contact_number=kwargs.get('pass'))
    if patient:
        serializer = PatientProfileSerializers(patient, many=False)
        bed = PatientBed.objects.filter(patient = patient, bed_status=True)
        data = serializer.data
        if bed.exists():
            data["bed_number"] = bed.first().bed_id
        else:
            data["bed_number"] = "NA"
        
            
        # print(serializer.data)
        data = {'data' : data,  'status' :status.HTTP_200_OK }
        return Response(data)
    else:
        return Response({'data': "Patient  doesn't exits ", 'status': status.HTTP_404_NOT_FOUND})



@permission_classes([IsAuthenticated])
@api_view(['POST'])
def bed_allotment(request):
    serializer = PatientBedSerializers( data = request.data)    
    if serializer.is_valid():
        serializer.save()
        return Response({"data": request.data , "status":status.HTTP_201_CREATED, "msg" : "Bed alloted to patient {}".format(request.data["patient_id"]) })
    else:
        return Response({"data": serializer.errors, "status" : status.HTTP_400_BAD_REQUEST })


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def get_alloted_beds(request, **kwargs):
    tbed = BedCount.objects.all()
    if tbed.count() == 0:
        return Response({'data': "beds are not available", 'status': status.HTTP_404_NOT_FOUND})
    
    total_bed = tbed[0].total
    total_gen = tbed[0].general
    total_oxy = tbed[0].oxygen
    total_icu = tbed[0].icu
    total_venti = tbed[0].ventillator
    total_alloted_bed = PatientBed.objects.filter(bed_status=True)
    general_bed = PatientBed.objects.filter(bed_status=True, bed_category="1")
    oxy_bed = PatientBed.objects.filter(bed_status=True, bed_category="2")
    icu_bed = PatientBed.objects.filter(bed_status=True, bed_category="3")
    ventillator_bed = PatientBed.objects.filter(bed_status=True, bed_category="4")
    serializers = PatientBedSerializers(total_alloted_bed, many=True)

    # for count of patients
    total_recovered = PatientProfile.objects.filter(patient_status="R",)
    total_migrated = PatientProfile.objects.filter(patient_status="M",)
    total_death = PatientProfile.objects.filter(patient_status="D",)
    total_isolated = PatientProfile.objects.filter(patient_status="H", )
    total_active = PatientProfile.objects.filter(patient_status = 'A',  )
    patient_status = { "recovered" : total_recovered.count() , 
            "migrated" : total_migrated.count(),
            "death" : total_death.count(),
            "isolated" : total_isolated.count(),
            "active" : total_active.count(),
            }

    alloted_beds = { "total" : total_alloted_bed.count() , 
            "general" : general_bed.count(),
            "oxygen" : oxy_bed.count(),
            "icu" : icu_bed.count(),
            "ventillator" : ventillator_bed.count()
            }
            
    total_beds = {
        "total" : total_bed,
        "general" : total_gen,
        "oxygen" : total_oxy,
        "icu" : total_icu,
        "ventillator" : total_venti  }

    data = {"data": serializers.data, "alloted_beds": alloted_beds, "total_beds": total_beds, "patient_status": patient_status, "status": status.HTTP_200_OK}

    return Response(data)


@permission_classes([IsAuthenticated])
@api_view(["PATCH"])
def change_patient_status(request, **kwargs):
    object = get_object_or_404(PatientProfile, patient_id = kwargs.get("id"))
    serializer = PatientStatusSerializer(data=request.data)

    if serializer.is_valid():        
        object.patient_status = serializer.data.get("patient_status")
        object.save()         

        if serializer.data.get("patient_status") == "A" and request.data["patient_bed"] !={} and  serializer.data.get("patient_bed")["bed_number"] != None :
            bed = PatientBed(patient=object)
            bed_id = "W{0}-F{1}-{2}".format(serializer.data.get("patient_bed")["ward"], serializer.data.get("patient_bed")["floor"], serializer.data.get("patient_bed")["bed_number"])
            bed.bed_id = bed_id
            bed.bed_number = serializer.data.get("patient_bed")["bed_number"]
            bed.bed_category = serializer.data.get("patient_bed")["bed_category"]
            bed.floor = serializer.data.get("patient_bed")["floor"]
            bed.ward = serializer.data.get("patient_bed")["ward"]
            bed.save()
        
        response = {
            'status': status.HTTP_200_OK,
            'data' : object.get_patient_status_display(),
            'msg': 'Patient status updated successfully',            
        }

        return Response(response)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""""
  Patient Migrations to another Covid facility
"""
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def patient_migrate_status(request, **kwargs):
     
    serializer = PatientMigrateSerializers(data=request.data)
    if serializer.is_valid():        
        serializer.save()
        response = {
          "data" : serializer.data, "status" : status.HTTP_201_CREATED       
        }
        
        return Response(response)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



""""
  Patient Death
"""
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def patient_death_status(request, **kwargs):
     
    serializer = PatientDeathSerializers(data=request.data)
    if serializer.is_valid():        
        serializer.save()
        response = {
          "data" : serializer.data, "status" : status.HTTP_201_CREATED       
        }
        
        return Response(response)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_filter_patients(request, **kwargs):
    pstatus = kwargs.get("status")
    patient_profile = PatientProfile.objects.filter(patient_status=pstatus)
    serializers = PatientProfileSerializers(patient_profile, many=True)
    if patient_profile.count()!=0:
        return Response({"data": serializers.data, "status": status.HTTP_200_OK})
    else:
        return Response({"data": "Not Found!", "status": status.HTTP_404_NOT_FOUND})


@api_view(["GET"])
def get_patient_count(request, **kwargs):
    patient_profile = PatientProfile.objects.all().annotate(x=TruncDay('admitted_on')).values("x").annotate(y=Count('id')).order_by("-admitted_on")
    if patient_profile.count()!=0:
        return Response({"data": patient_profile , "status": status.HTTP_200_OK})
    else:
        return Response({"data": "Not Found!", "status": status.HTTP_404_NOT_FOUND})
from django.shortcuts import render
# third party imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404 
from.models import *
from rest_framework.decorators import api_view, permission_classes
from django.utils.timezone import datetime
User = settings.AUTH_USER_MODEL


class EventsView(APIView):
    def get(self, request, *args, **kwargs):      
        events = Events.objects.all()
        serializers = EventListSerializers(events, many=True)
        data =   {'data': serializers.data, 'msg' : 'Events listed', 'status': status.HTTP_200_OK }      
        if events.exists():                         
            return Response(data)
        else:
            return Response({'data': [] , 'msg' : "No Events added", 'status': status.HTTP_404_NOT_FOUND})


 


@api_view(['GET'])
def get_event(request, **kwargs):
    id = kwargs.get('id')
    qs  = Events.objects.all().filter(id = id)
    serializer = EventListSerializers(qs, many=True)
    if qs.exists():        
        return Response({"data": serializer.data,  'msg' : "Search Result Found", "status": status.HTTP_200_OK })
    else:
        return Response({'data': [],  'msg' : "Searched result not found :-( ", 'status': status.HTTP_404_NOT_FOUND})


@api_view(['GET'])
def filter_events(request, **kwargs):
    event_type = kwargs.get('type')
    event_status = kwargs.get('status')
    qs  = Events.objects.all()
    if event_type:
        qs = qs.filter(type=event_type)
    if event_status and qs.exists():
        qs =   qs.filter(status = event_status)

    serializer = EventListSerializers(qs, many=True)
    if qs.exists():        
        return Response({"data": serializer.data,  'msg' : "Search Result Found", "status": status.HTTP_200_OK })
    else:
        return Response({'data': [],  'msg' : "Searched result not found :-( ", 'status': status.HTTP_404_NOT_FOUND})

 

@api_view(['GET'])
def filter_event_type(request, **kwargs):
    event_type = kwargs.get('type')
    qs  = Events.objects.all().filter(type = event_type)
    serializer = EventListSerializers(qs, many=True)
    if qs.exists():        
        return Response({"data": serializer.data, "status": status.HTTP_200_OK })
    else:
        return Response({'data':[] , 'msg' : "Searched result not found :-( ", 'status': status.HTTP_404_NOT_FOUND})

 


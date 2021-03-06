from django.shortcuts import render
# third party imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404 
from.models import *
from django.utils.timezone import datetime
User = settings.AUTH_USER_MODEL



@api_view(['GET'])
def filter_contestants(request, **kwargs):
    event = kwargs.get("id")
    player = Contestants.objects.all().filter( events__type = 0, events__id = event)
    # player = Contestants.objects.all()

    serializers = ContestantsListSerializers(player, many=True, context = { "event_id" : event})
    data =   {'data': serializers.data, 'msg' : 'filtered constestants listed', 'status': status.HTTP_200_OK }      
    if player.exists():                         
        return Response(data)
    else:
        return Response({'data': [] , 'msg' : "No Contestants", 'status': status.HTTP_404_NOT_FOUND})


@api_view(['GET'])
def filter_team(request, **kwargs):
    event = kwargs.get("id")
    team = Teams.objects.all().filter(event__id = event)
    # team = Teams.objects.all()
    serializers = TeamListSerializers(team, many=True)
    data =   {'data': serializers.data, 'msg' : "Filtered Team listed", 'status': status.HTTP_200_OK }      
    if team.exists():                         
        return Response(data)
    else:
        return Response({'data': [] , 'msg' : "No Team", 'status': status.HTTP_404_NOT_FOUND})


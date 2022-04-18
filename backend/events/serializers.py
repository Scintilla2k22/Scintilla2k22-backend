from numpy import source
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import fields
from .models import *
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User




class CoordinatesSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source = "first_name")
    class Meta:
        model = Coordinators
        fields = ('id', 'name',  'email', 'username', 'gender', 'branch', 'year', 'contact_number')


class EventListSerializers(serializers.ModelSerializer):
    
    co_ord = CoordinatesSerializers(many=True)
    class Meta:
        model = Events
        fields = ( 'id', 'e_name','code', 'e_desc', 'co_ord', 'status', 'e_time', 'image', 'url', 'type')    




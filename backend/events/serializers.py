from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import fields
from rest_framework.fields import NOT_READ_ONLY_WRITE_ONLY
from .models import *
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User




class CoordinatesSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')


class EventListSerializers(serializers.ModelSerializer):
    
    co_ord = CoordinatesSerializers(many=True)
    class Meta:
        model = Events
        fields = ( 'id', 'e_name','code', 'e_desc', 'co_ord', 'status', 'e_time', 'image', 'url', 'type')    




from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import fields
from rest_framework.fields import NOT_READ_ONLY_WRITE_ONLY
from .models import *
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL





class EventListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ( 'id', 'e_name', 'e_desc', 'co_ord', 'status', 'e_time', 'image')    




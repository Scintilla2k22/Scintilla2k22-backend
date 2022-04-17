from dataclasses import field
from pyexpat import model
from pkg_resources import require
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import fields
from rest_framework.fields import NOT_READ_ONLY_WRITE_ONLY
from .models import *
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL




class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = 'score'


class ContestantsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contestants
        fields = '__all__'    
        
        # fields = ('id', 'name', 'branch', 'year', 'created_on')    


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = 'score'


class TeamListSerializers(serializers.ModelSerializer):
    
    contestants = ContestantsListSerializers(many=True)
    class Meta:
        model = Teams
        # fields = ('id', 't_name', 'contestants', 'event', 'image', "created_on")
        fields = '__all__'    
           


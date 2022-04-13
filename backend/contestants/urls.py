from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
path('get_contestants/<str:id>/', filter_contestants , name = "get_contestants"),
path('get_team/<str:id>/', filter_team, name = "get_team"),


]
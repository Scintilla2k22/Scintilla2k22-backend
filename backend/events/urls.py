from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
path('get_events/', EventsView.as_view(), name = "get_events"),
path('filter_event_type/<str:type>/', filter_event_type, name = "filter_event_type"),
path('filter_events/<str:type>/<str:status>/', filter_events, name = "filter_events"),


]
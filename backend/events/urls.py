from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
path('get_events/', EventsView.as_view(), name = "get_events"),
path('get_event/<str:id>/', get_event, name = "get_event"),
path('filter_event_status/<str:status>/', filter_event_status, name = "filter_event_status"),
path('filter_events/<str:type>/<str:status>/', filter_events, name = "filter_events"),


]
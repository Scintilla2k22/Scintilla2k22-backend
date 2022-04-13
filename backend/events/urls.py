from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
path('get-events/', EventsView.as_view(), name = "get_events"),
path('filter_events/<str:type>/<str:status>/', filter_events, name = "filter_events"),


]
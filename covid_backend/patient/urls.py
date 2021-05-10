from django.urls import path, include
from .views import *

urlpatterns = [

    # path('register/', PatientAdmissionView.as_view(), name="register"),
    path('admit/', PatientProfileView.as_view(), name="profile"),
   
]
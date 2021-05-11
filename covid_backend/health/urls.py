from django.urls import path, include
from .views import *

urlpatterns = [

    # path('register/', PatientAdmissionView.as_view(), name="register"),
    path('update/', PatientHealthUpdateView.as_view(), name="update"),
    path('details/<str:icmr>/', get_patients, name="get_patients")
    
]
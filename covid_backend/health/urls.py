from django.urls import path, include
from .views import *

urlpatterns = [

    # path('register/', PatientAdmissionView.as_view(), name="register"),
    path('update/', PatientHealthUpdateView.as_view(), name="update"),
    path('details/<str:icmr>/', get_patients_health, name="get_patients_health"),

    # paginated data 
    path('patient_health_list/<str:icmr>/', PatientHealthStatusList.as_view(), name="patient_health_list")

]
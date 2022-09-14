from django.urls import path, include
from .views import *

urlpatterns = [

    # path('register/', PatientAdmissionView.as_view(), name="register"),
    path('update/', PatientHealthUpdateView.as_view(), name="update"),
    path('details/<str:icmr>/', get_patients_health, name="get_patients_health"),
    path('oxy_level/<str:icmr>/', get_patients_oxy_level, name="get_patients_oxy_level"),
    path('temperature_level/<str:icmr>/', get_patients_temperature_level, name="get_patients_temperature_level"),
    path('respiratory_rate/<str:icmr>/', get_patients_respiratory_rate, name="get_patients_respiratory_rate"),
    path('bp_level/<str:icmr>/', get_patients_bp_level, name="get_patients_bp_level"),
    path('pulse_rate/<str:icmr>/', get_patients_pulse_rate, name="get_patients_pulse_rate"),
    path('readings/<str:icmr>/', get_patients_readings, name="get_patients_readings"),

    # paginated data 
    path('patient_health_list/<str:icmr>/', PatientHealthStatusList.as_view(), name="patient_health_list")

]
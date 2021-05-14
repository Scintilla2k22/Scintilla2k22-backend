from django.urls import path, include
from .views import *

urlpatterns = [

    # path('register/', PatientAdmissionView.as_view(), name="register"),
    path('admit/', PatientProfileView.as_view(), name="profile"),
    path('bed_allotment/', bed_allotment, name="bed_allotment" ),
    path('get_patient_profile/<str:id>/', get_patient_profile, name="get_patient_profile"),
    path('get_alloted_beds/', get_alloted_beds, name="get_alloted_beds"),
    path('change_patient_status/<str:id>/', change_patient_status, name="change_patient_status"),
    path('change_covid_facility/<str:id>/', change_covid_facility, name="change_covid_facility"),
    path('get_filter_patients/<str:status>/', get_filter_patients, name="get_filter_patients")

]
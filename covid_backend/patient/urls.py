from django.urls import path, include
from .views import *

urlpatterns = [

    # path('register/', PatientAdmissionView.as_view(), name="register"),
    path('admit/', PatientProfileView.as_view(), name="profile"),
    path('bed_allotment/', bed_allotment, name="bed_allotment" ),
    path('get_patient_profile/<str:id>/', get_patient_profile, name="get_patient_profile"),
    path('get_alloted_beds/', get_alloted_beds, name="get_alloted_beds")

]
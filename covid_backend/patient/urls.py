from django.urls import path, include
from .views import *

urlpatterns = [

    path('register/', PatientAdmissionView.as_view(), name="register"),
    path('profile/', PatientProfileView.as_view(), name="profile"),
    # path('profile/passwordchange/', ChangePasswordView.as_view(), name="reset_password"),
    # path('login/', LoginUserView.as_view(), name="login"),
    # path('logout/', LogoutUserView.as_view(), name="logout"),
    # path('contact/', ContactUsView.as_view(), name="contact"),
 
]
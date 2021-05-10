from django.urls import path, include
from .views import *

urlpatterns = [

    path('register/', MedicalStaffRegistrationView.as_view(), name="register"),
    path('profile/', MedicalStaffProfileView.as_view(), name="profile"),
    path('profile/passwordchange/', ChangePasswordView.as_view(), name="reset_password"),
    path('login/', LoginUserView.as_view(), name="login"),
    path('logout/', LogoutUserView.as_view(), name="logout"),

]
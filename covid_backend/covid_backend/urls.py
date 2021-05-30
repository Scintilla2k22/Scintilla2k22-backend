"""covid_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/staff/', include('user.urls') ),
    path('api/patient/', include('patient.urls')),
    path('api/health/', include('health.urls'))
    #  path('api/health/', include('health.urls')),
]
admin.site.site_header = 'GTR Base Hospital Almora'                    # default: "Django Administration"
admin.site.index_title = 'Patient Details'                 # default: "Site administration"
admin.site.site_title = 'GTR Base Hospital Almora'
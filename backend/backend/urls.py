from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/participants/', include('contestants.urls')),
    path('api/events/', include('events.urls')),

]

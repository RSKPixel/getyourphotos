from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('gyp/', include('gyp.urls')),
]

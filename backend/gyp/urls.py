from django.urls import path
from gyp import views

urlpatterns = [
    path('upload/', views.upload)
]

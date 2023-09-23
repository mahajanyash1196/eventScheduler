from django.contrib import admin
from django.urls import path,include
from emailSender import views

urlpatterns = [
    path('send/email', views.send_email),
]

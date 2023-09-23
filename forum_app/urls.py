from django.contrib import admin
from django.urls import path
from .views import OpenMainWeb
from . import views

urlpatterns = [
    path('main', views.OpenMainWeb),
]

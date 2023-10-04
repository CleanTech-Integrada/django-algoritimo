from django.contrib import admin
from django.urls import path, include
from .views import home
from .conrollers.AlgoritimoController import index

urlpatterns = [
    path('', index),
]
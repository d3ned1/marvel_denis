from django.contrib import admin
from django.urls import path, include
from marvel_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('marvel/', views.marvel, name="marvel"),
    path('master/', views.master, name="master"),
    path('comics/', views.comics, name="comics"),
    path('about/', views.about, name="about"),
]

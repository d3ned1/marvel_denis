from django.contrib import admin
from django.urls import path, include
from marvel_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.marvel, name="marvel"),
    path('marvel/', views.marvel, name="marvel"),
    path('comics/', views.comics, name="comics"),
    path('about/', views.about, name="about"),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
]

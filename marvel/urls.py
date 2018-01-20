from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import login, logout
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('marvel_app.urls')),
]
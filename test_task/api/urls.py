from django.contrib import admin
from django.urls import path, include, re_path
from api import views

urlpatterns = [
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
]
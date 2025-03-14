"""
URLs for the user application.
This module contains the URL patterns for the user application.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('api/', include(router.urls)),
]

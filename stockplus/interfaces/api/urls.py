"""
URL configuration for the API.
This module contains the URL patterns for the API.
"""

from django.urls import path, include

from stockplus.interfaces.api.views import (
    UserCreateAPIView,
    UserProfileAPIView,
    UserVerifyAPIView
)

# User URLs
user_urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('<int:pk>/profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('verify/', UserVerifyAPIView.as_view(), name='user-verify'),
]

# API URLs
urlpatterns = [
    path('users/', include(user_urlpatterns)),
]

"""
URL configuration for the user application.
This module contains the URL patterns for the user application.
"""

from django.urls import path

from builder.modules.user.interfaces.views.create import UserCreateView
from builder.modules.user.interfaces.views.details import UserDetailView
from builder.modules.user.interfaces.views.invitation import InvitationCreateView, InvitationValidateView
from builder.modules.user.interfaces.views.email_verify import EmailVerifyView, ResendVerificationEmailView


urlpatterns = [
    # User URLs
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('profile/', UserDetailView.as_view(), name='user-profile'),
    
    # Invitation URLs
    path('invitations/', InvitationCreateView.as_view(), name='invitation-create'),
    path('invitations/<str:token>/validate/', InvitationValidateView.as_view(), name='invitation-validate'),
    
    # Email verification URLs
    path('verify-email/', EmailVerifyView.as_view(), name='email-verify'),
    path('resend-verification-email/', ResendVerificationEmailView.as_view(), name='resend-verification-email'),
]

"""
URL configuration for the user application.
This module contains the URL patterns for the user application.
"""

from django.urls import path

from builder.modules.user.interfaces.views.create import UserCreateView
from builder.modules.user.interfaces.views.details import UserDetailView
from builder.modules.user.interfaces.views.invitation import InvitationCreateView, InvitationValidateView
from builder.modules.user.interfaces.views.email_verify import EmailVerifyView, ResendVerificationEmailView
from builder.modules.user.interfaces.views.auth import (
    LoginView, LogoutView, RefreshTokenView,
    ForgotPasswordView, ResetPasswordView
)


urlpatterns = [
    # User URLs
    path('api/users/profile/', UserDetailView.as_view(), name='user-profile'),

    # Authentication URLs
    path('api/auth/register/', UserCreateView.as_view(), name='user-register'),
    path('api/auth/login/', LoginView.as_view(), name='auth-login'),
    path('api/auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('api/auth/refresh-token/', RefreshTokenView.as_view(), name='auth-refresh-token'),
    path('api/auth/forgot-password/', ForgotPasswordView.as_view(), name='auth-forgot-password'),
    path('api/auth/reset-password/', ResetPasswordView.as_view(), name='auth-reset-password'),

    # Invitation URLs
    path('api/auth/invitations/', InvitationCreateView.as_view(), name='invitation-create'),
    path('api/auth/invitations/<str:token>/validate/', InvitationValidateView.as_view(), name='invitation-validate'),

    # Email verification URLs
    path('api/auth/verify-email/', EmailVerifyView.as_view(), name='email-verify'),
    path('api/auth/resend-verification-email/', ResendVerificationEmailView.as_view(), name='resend-verification-email'),
]

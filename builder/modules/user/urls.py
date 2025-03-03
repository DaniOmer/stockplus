"""
URL configuration for the user application.
This module contains the URL patterns for the user application.
"""

from django.urls import path

from builder.modules.user.interfaces.views import (
    AccountView,
    AvatarUploadView,
    UserCreateView,
    UserDetailView,
    EmailVerifyView,
    ResendVerificationEmailView,
    InvitationCreateView,
    InvitationValidateView,
    NotificationDeleteView,
    NotificationListView,
    NotificationMarkAsReadView,
    LoginView,
    LogoutView,
    ChangePasswordView,
    RefreshTokenView,
    ForgotPasswordView,
    ResetPasswordView,
)

urlpatterns = [
    # User URLs
    path('api/users/profile/', UserDetailView.as_view(), name='user-profile'),
    path('api/users/change-password/', ChangePasswordView.as_view(), name='user-change-password'),
    path('api/users/account/', AccountView.as_view(), name='user-account'),
    path('api/users/avatar/', AvatarUploadView.as_view(), name='user-avatar'),
    
    # Notification URLs
    path('api/users/notifications/', NotificationListView.as_view(), name='user-notifications'),
    path('api/users/notifications/mark-read/', NotificationMarkAsReadView.as_view(), name='user-notifications-mark-read'),
    path('api/users/notifications/mark-read/<int:notification_id>/', NotificationMarkAsReadView.as_view(), name='user-notification-mark-read'),
    path('api/users/notifications/delete/', NotificationDeleteView.as_view(), name='user-notifications-delete'),
    path('api/users/notifications/delete/<int:notification_id>/', NotificationDeleteView.as_view(), name='user-notification-delete'),

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

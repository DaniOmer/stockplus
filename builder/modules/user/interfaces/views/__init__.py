"""
Interfaces layer for the user application.
This package contains the views for the user application.
"""

from builder.modules.user.interfaces.views.account import AccountView
from builder.modules.user.interfaces.views.avatar import AvatarUploadView
from builder.modules.user.interfaces.views.create import UserCreateView
from builder.modules.user.interfaces.views.details import UserDetailView
from builder.modules.user.interfaces.views.password import ChangePasswordView
from builder.modules.user.interfaces.views.email_verify import EmailVerifyView, ResendVerificationEmailView
from builder.modules.user.interfaces.views.invitation import InvitationCreateView, InvitationValidateView
from builder.modules.user.interfaces.views.notification import NotificationDeleteView, NotificationListView, NotificationMarkAsReadView
from builder.modules.user.interfaces.views.auth import LoginView, LogoutView, RefreshTokenView, ForgotPasswordView, ResetPasswordView

__all__ = [
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
]
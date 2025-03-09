"""
Authentication views for the user application.
This module contains the authentication views for the user application.
"""

from stockplus.modules.user.interfaces.views.auth.register import RegisterView
from stockplus.modules.user.interfaces.views.auth.login import LoginView
from stockplus.modules.user.interfaces.views.auth.logout import LogoutView
from stockplus.modules.user.interfaces.views.auth.refresh_token import RefreshTokenView
from stockplus.modules.user.interfaces.views.auth.forgot_password import ForgotPasswordView
from stockplus.modules.user.interfaces.views.auth.reset_password import ResetPasswordView

__all__ = [
    RegisterView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    ForgotPasswordView,
    ResetPasswordView
]
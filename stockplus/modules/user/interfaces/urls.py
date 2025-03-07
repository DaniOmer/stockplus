"""
URL configuration for the user application.
This module contains the URL configuration for the user application.
"""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Import from the auth.py file
from stockplus.modules.user.interfaces.views.auth_file import RegisterView, LoginView
from stockplus.modules.user.interfaces.views.email_verify import (
    EmailVerifyView,
    ResendVerificationEmailView,
)
from stockplus.modules.user.interfaces.views.password_reset import (
    PasswordResetRequestView,
    PasswordResetVerifyView,
    PasswordResetConfirmView,
)
from stockplus.modules.user.interfaces.views.profile import UserProfileView

urlpatterns = [
    # Authentication
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    
    # JWT Tokens
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Email Verification
    path('api/auth/email-verify/', EmailVerifyView.as_view(), name='email-verify'),
    path('api/auth/email-verify/resend/', ResendVerificationEmailView.as_view(), name='email-verify-resend'),
    
    # Password Reset
    path('api/auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('api/auth/password-reset/verify/', PasswordResetVerifyView.as_view(), name='password-reset-verify'),
    path('api/auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # User Profile
    path('api/user/profile/', UserProfileView.as_view(), name='user-profile'),
]

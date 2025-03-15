"""
Authentication views for the user application.
This module contains the authentication views for the user application.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from stockplus.infrastructure.api.mixins import ResponseFormatterMixin
from stockplus.modules.user.application.services import TokenService, UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository, TokenRepository
from stockplus.modules.user.interfaces.serializers import (
    UserBaseSerializer,
    UserCreateSerializer,
    LoginSerializer,
    LogoutSerializer,
    EmailVerifySerializer,
    ResendVerificationEmailSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    PasswordUpdateSerializer,
)
from stockplus.modules.user.infrastructure.utils import generate_jwt_access_and_refresh_token, blacklist_token

class AuthViewSet(ResponseFormatterMixin, viewsets.ViewSet):
    """
    ViewSet for user authentication.
    """
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService(UserRepository(), TokenService(TokenRepository()))
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        if self.action == 'register':
            return UserCreateSerializer
        elif self.action == 'login':
            return LoginSerializer
        elif self.action == 'logout':
            return LogoutSerializer
        elif self.action == 'verify_email':
            return EmailVerifySerializer
        elif self.action == 'resend_verification':
            return ResendVerificationEmailSerializer
        elif self.action == 'request_password_reset':
            return PasswordResetRequestSerializer
        elif self.action == 'confirm_password_reset':
            return PasswordResetConfirmSerializer
        elif self.action == 'update_password':
            return PasswordUpdateSerializer
        return super().get_serializer_class()
    
    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    @action(detail=False, methods=['post'])
    def register(self, request, *args, **kwargs):
        """
        Create a new user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_service = UserService(UserRepository(), TokenService(TokenRepository()))
        user = user_service.create_user(**serializer.validated_data)
        return self.format_response(
            data=UserBaseSerializer(user).data,
            message="User created successfully",
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Login user and return tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.user_service.login(**serializer.validated_data)
        tokens = generate_jwt_access_and_refresh_token(user)
        return Response(
            {
                'user': {
                    **UserBaseSerializer(user).data,
                    'company': user.company
                },
                **tokens,
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def verify_email(self, request):
        """
        Verify user email.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.user_service.verify_email(**serializer.validated_data)
        
        return self.format_response(
            message="Email verified successfully",
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def resend_verification(self, request):
        """
        Resend verification email.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.user_service.resend_verification(**serializer.validated_data)
        
        return self.format_response(
            message="Verification email sent successfully",
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def request_password_reset(self, request):
        """
        Request password reset.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.user_service.request_password_reset(**serializer.validated_data)
        
        return self.format_response(
            message="Password reset email sent successfully",
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def confirm_password_reset(self, request):
        """
        Confirm password reset.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.user_service.confirm_password_reset(**serializer.validated_data)
        
        return self.format_response(
            message="Password reset successfully",
            status=status.HTTP_200_OK
        )
        
    @action(detail=False, methods=['post'])
    def update_password(self, request):
        """
        Update user password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.user_service.update_password(
            user_id=request.user.id,
            **serializer.validated_data
        )
        
        return self.format_response(
            message="Password updated successfully",
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Logout user by blacklisting the refresh token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        blacklist_token(serializer.validated_data['refresh_token'])

        return self.format_response(
            message="Logged out successfully",
            status=status.HTTP_200_OK
        )

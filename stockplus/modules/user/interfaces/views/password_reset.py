"""
Password reset views for the user application.
This module contains the password reset views for the user application.
"""

import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from stockplus.modules.user.application.user_service import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.interfaces.serializers.auth import (
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    PasswordResetConfirmSerializer
)
from stockplus.modules.messenger.infrastructure.utils import send_mail_message
from stockplus.modules.user.domain.exceptions import (
    UserNotFoundException,
    TokenInvalidException,
    TokenExpiredException
)

logger = logging.getLogger(__name__)

class PasswordResetRequestView(generics.GenericAPIView):
    """
    API endpoint to request a password reset.
    
    This endpoint generates a password reset token and sends it to the user's
    email address. Password reset is only available via email.
    For security reasons, it always returns a success message, even if the
    account doesn't exist, to prevent user enumeration attacks.
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Request a password reset.

        Args:
            request: The request containing the user's email

        Returns:
            Response: The response indicating that a reset link has been sent (if the account exists)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        
        # Email is required for password reset
        if not email:
            return Response({
                'message': 'Email is required for password reset'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the user service
        user_service = UserService(UserRepository())
        
        try:
            # Get the user
            user = user_service.get_user_by_email(email)
            
            if not user:
                # Don't reveal that the user doesn't exist
                logger.info(f"Password reset requested for non-existent account: {email}")
                return Response({
                    'message': 'If your account exists, a password reset link has been sent'
                }, status=status.HTTP_200_OK)
            
            # Generate a password reset token
            token = user_service.generate_password_reset_token(email=email)
            
            # Create a reset URL
            from django.urls import reverse
            from django.conf import settings
            from django.template.loader import render_to_string
            
            reset_link = reverse('password-reset-confirm')
            reset_url = f"{settings.FRONTEND_URL}{reset_link}?token={token}"
            
            html_content = render_to_string('password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
                'token': token
            })
            
            # Send the password reset email
            send_mail_message(
                subject='Reset Your Password',
                target=email,
                template='password_reset_email.html',
                html=html_content,
                message=f'Your password reset code is: {token}'
            )
            
            logger.info(f"Password reset email sent to: {email}")
            
            return Response({
                'message': 'If your account exists, a password reset link has been sent'
            }, status=status.HTTP_200_OK)
        except UserNotFoundException as e:
            # Don't reveal that the user doesn't exist
            logger.warning(f"Password reset failed: {str(e)}. Email: {email}")
            return Response({
                'message': 'If your account exists, a password reset link has been sent'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the error but don't reveal specific details to the user
            logger.error(f"Password reset failed with unexpected error: {str(e)}", exc_info=True)
            return Response({
                'message': 'If your account exists, a password reset link has been sent'
            }, status=status.HTTP_200_OK)


class PasswordResetVerifyView(generics.GenericAPIView):
    """
    API endpoint to verify a password reset token.
    
    This endpoint verifies that a password reset token is valid before
    allowing the user to proceed with resetting their password.
    """
    serializer_class = PasswordResetVerifySerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Verify a password reset token.

        Args:
            request: The request containing the token to verify

        Returns:
            Response: The response indicating whether the token is valid
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        
        # Create the user service
        user_service = UserService(UserRepository())
        
        try:
            # Verify the token
            token_data = user_service.verify_password_reset_token(token)
            
            if token_data.get('type') != 'password_reset':
                return Response({
                    'message': 'Invalid token type. This token is not for password reset.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get the user ID from the token data
            user_id = token_data['user_id']
            
            return Response({
                'message': 'Token verified successfully',
                'token': token,
                'user_id': user_id
            }, status=status.HTTP_200_OK)
        except (TokenInvalidException, TokenExpiredException) as e:
            logger.warning(f"Password reset token verification failed: {str(e)}. Token: {token}")
            return Response({
                'message': str(e),
                'error_code': 'invalid_token' if isinstance(e, TokenInvalidException) else 'expired_token'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Password reset token verification failed with unexpected error: {str(e)}", exc_info=True)
            return Response({
                'message': 'An unexpected error occurred. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    API endpoint to confirm a password reset.
    
    This endpoint resets a user's password using a valid password reset token.
    It verifies the token, updates the password, and invalidates the token.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Confirm a password reset.

        Args:
            request: The request containing the token and new password

        Returns:
            Response: The response indicating whether the password was reset successfully
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        # Create the user service
        user_service = UserService(UserRepository())
        
        try:
            # Reset the password
            user = user_service.reset_password(token, new_password)
            
            return Response({
                'message': 'Password reset successfully',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_200_OK)
        except UserNotFoundException as e:
            logger.warning(f"Password reset confirmation failed: User not found. Token: {token}")
            return Response({
                'message': 'User not found. The account may have been deleted.'
            }, status=status.HTTP_404_NOT_FOUND)
        except (TokenInvalidException, TokenExpiredException) as e:
            logger.warning(f"Password reset confirmation failed: {str(e)}. Token: {token}")
            return Response({
                'message': str(e),
                'error_code': 'invalid_token' if isinstance(e, TokenInvalidException) else 'expired_token'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Password reset confirmation failed with unexpected error: {str(e)}", exc_info=True)
            return Response({
                'message': 'An unexpected error occurred. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""
Password reset views for the user application.
This module contains the password reset views for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from stockplus.modules.user.application.services import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.interfaces.serializers.auth import (
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    PasswordResetConfirmSerializer
)
from stockplus.modules.messenger.infrastructure.utils import send_mail_message, send_sms_message
from stockplus.modules.user.domain.exceptions import (
    UserNotFoundException,
    TokenInvalidException,
    TokenExpiredException
)


class PasswordResetRequestView(generics.GenericAPIView):
    """
    API endpoint to request a password reset.
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Request a password reset.

        Args:
            request: The request

        Returns:
            Response: The response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')
        reset_method = serializer.validated_data.get('reset_method', 'email')
        
        # Create the user service
        user_service = UserService(UserRepository())
        
        try:
            # Generate a password reset token
            token = user_service.generate_password_reset_token(email=email, phone_number=phone_number)
            
            # Get the user
            user = None
            if email:
                user = user_service.get_user_by_email(email)
            elif phone_number:
                user = user_service.get_user_by_phone_number(phone_number)
            
            if not user:
                # Don't reveal that the user doesn't exist
                return Response({
                    'message': 'If your account exists, a password reset link has been sent'
                }, status=status.HTTP_200_OK)
            
            # Send the password reset code
            if reset_method == 'email' and email:
                # Create a reset URL
                reset_url = f"/reset-password?token={token}"
                
                send_mail_message(
                    subject='Reset Your Password',
                    target=email,
                    template='password_reset_email.html',
                    context={
                        'token': token,
                        'reset_url': reset_url
                    },
                    message=f'Your password reset code is: {token}'
                )
            elif reset_method == 'sms' and phone_number:
                send_sms_message(
                    to_phone=phone_number,
                    message=f'Your password reset code is: {token}'
                )
            else:
                return Response({
                    'message': 'Invalid reset method'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'message': 'If your account exists, a password reset link has been sent'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            # Don't reveal specific errors
            return Response({
                'message': 'If your account exists, a password reset link has been sent'
            }, status=status.HTTP_200_OK)


class PasswordResetVerifyView(generics.GenericAPIView):
    """
    API endpoint to verify a password reset token.
    """
    serializer_class = PasswordResetVerifySerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Verify a password reset token.

        Args:
            request: The request

        Returns:
            Response: The response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        
        # Create the user service
        user_service = UserService(UserRepository())
        
        try:
            # Verify the token
            token_data = user_service.verify_password_reset_token(token)
            
            return Response({
                'message': 'Token verified successfully',
                'token': token
            }, status=status.HTTP_200_OK)
        except (TokenInvalidException, TokenExpiredException) as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    API endpoint to confirm a password reset.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Confirm a password reset.

        Args:
            request: The request

        Returns:
            Response: The response
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
                'message': 'Password reset successfully'
            }, status=status.HTTP_200_OK)
        except UserNotFoundException as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)
        except (TokenInvalidException, TokenExpiredException) as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

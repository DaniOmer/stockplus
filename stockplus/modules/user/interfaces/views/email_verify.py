"""
Email verification views for the user application.
This module contains the email verification views for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from datetime import datetime, timedelta

from stockplus.modules.user.application.services import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.infrastructure.repositories.token_repository import get_token_repository
from stockplus.modules.user.interfaces.serializers.auth import EmailVerifySerializer, ResendVerificationEmailSerializer
from stockplus.modules.messenger.infrastructure.utils import send_mail_message, send_sms_message
from stockplus.modules.user.domain.exceptions import (
    UserNotFoundException,
    TokenInvalidException,
    TokenExpiredException
)


class EmailVerifyView(generics.GenericAPIView):
    """
    API endpoint to verify a user's email.
    """
    serializer_class = EmailVerifySerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Verify a user's email.

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
            token_data = user_service.verify_token(token)
            
            # Get the user
            user_id = token_data['user_id']
            
            # Verify the user
            user = user_service.verify_user(user_id)
            
            return Response({
                'message': 'Email verified successfully'
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


class ResendVerificationEmailView(generics.GenericAPIView):
    """
    API endpoint to resend a verification email.
    """
    serializer_class = ResendVerificationEmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Resend a verification email.

        Args:
            request: The request

        Returns:
            Response: The response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        verification_method = serializer.validated_data.get('verification_method', 'email')
        
        # Create the user service
        user_service = UserService(UserRepository())
        
        try:
            # Get the user
            user = user_service.get_user_by_email(email)
            if not user:
                return Response({
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)

            if user.is_verified:
                return Response({
                    'message': 'User is already verified'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Generate a verification token
            token = user_service._generate_verification_token(user.id, method=verification_method)
            
            # Send the verification code
            if verification_method == 'email':
                send_mail_message(
                    subject='Verify Your Email',
                    target=user.email,
                    template='verification_email.html',
                    html=f'<p>Your verification code is: <strong>{token}</strong></p>',
                    message=f'Your verification code is: {token}'
                )
            elif verification_method == 'sms':
                send_sms_message(
                    to_phone=user.phone_number,
                    message=f'Your verification code is: {token}'
                )
            else:
                return Response({
                    'message': 'Invalid verification method'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'message': 'Verification code sent successfully'
            }, status=status.HTTP_200_OK)
        except UserNotFoundException as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'message': f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

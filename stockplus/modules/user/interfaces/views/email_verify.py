"""
Email verification views for the user application.
This module contains the email verification views for the user application.
"""

import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from stockplus.modules.user.application.user_service import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.interfaces.serializers.auth import EmailVerifySerializer, ResendVerificationEmailSerializer
from stockplus.modules.messenger.infrastructure.utils import send_mail_message, send_sms_message
from stockplus.modules.user.domain.exceptions import (
    UserNotFoundException,
    TokenInvalidException,
    TokenExpiredException
)

logger = logging.getLogger(__name__)

class EmailVerifyView(generics.GenericAPIView):
    """
    API endpoint to verify a user's email.
    
    This endpoint verifies a user's email using a token that was sent to their email address.
    The token is validated, and if valid, the user's email is marked as verified.
    """
    serializer_class = EmailVerifySerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Verify a user's email.

        Args:
            request: The request containing the verification token

        Returns:
            Response: The response indicating success or failure
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        
        # Create the user service
        user_service = UserService(UserRepository())
        
        try:
            # Verify the token
            token_data = user_service.verify_token(token)
            
            if token_data.get('type') != 'verification':
                return Response({
                    'message': 'Invalid token type. This token is not for email verification.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get the user
            user_id = token_data['user_id']
            
            # Verify the user
            user = user_service.verify_user(user_id)
            
            return Response({
                'message': 'Email verified successfully',
                'user_id': user.id,
                'email': user.email,
                'is_verified': user.is_verified
            }, status=status.HTTP_200_OK)
        except UserNotFoundException as e:
            logger.warning(f"Email verification failed: User not found. Token: {token}")
            return Response({
                'message': 'User not found. The account may have been deleted.'
            }, status=status.HTTP_404_NOT_FOUND)
        except (TokenInvalidException, TokenExpiredException) as e:
            logger.warning(f"Email verification failed: {str(e)}. Token: {token}")
            return Response({
                'message': str(e),
                'error_code': 'invalid_token' if isinstance(e, TokenInvalidException) else 'expired_token'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Email verification failed with unexpected error: {str(e)}", exc_info=True)
            return Response({
                'message': 'An unexpected error occurred. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResendVerificationEmailView(generics.GenericAPIView):
    """
    API endpoint to resend a verification email or SMS.
    
    This endpoint generates a new verification token and sends it to the user's
    email address or phone number, depending on the verification method selected.
    """
    serializer_class = ResendVerificationEmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Resend a verification email or SMS.

        Args:
            request: The request containing the user's email and verification method

        Returns:
            Response: The response indicating success or failure
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
                logger.warning(f"Verification resend failed: User not found. Email: {email}")
                return Response({
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)

            if user.is_verified:
                logger.info(f"Verification resend skipped: User already verified. Email: {email}")
                return Response({
                    'message': 'Your account is already verified. You can log in now.',
                    'is_verified': True
                }, status=status.HTTP_200_OK)

            # Generate a verification token
            token = user_service._generate_verification_token(user.id, method=verification_method)
            
            # Send the verification code
            if verification_method == 'email':
                if not user.email:
                    return Response({
                        'message': 'User does not have an email address'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
                # Render the email template with the token
                from django.template.loader import render_to_string
                from django.urls import reverse
                from django.conf import settings
                
                verification_link = reverse('email-verify')
                verification_url = f"{settings.FRONTEND_URL}{verification_link}?token={token}"
                html_content = render_to_string('verification_email.html', {
                    'user': user,
                    'verification_url': verification_url,
                    'token': token
                })
                
                send_mail_message(
                    subject='Verify Your Email',
                    target=user.email,
                    template='verification_email.html',
                    html=html_content,
                    message=f'Your verification code is: {token}'
                )
                
                logger.info(f"Verification email sent to: {user.email}")
            elif verification_method == 'sms':
                if not user.phone_number:
                    return Response({
                        'message': 'User does not have a phone number'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
                send_sms_message(
                    to_phone=user.phone_number,
                    message=f'Your verification code is: {token}'
                )
                
                logger.info(f"Verification SMS sent to: {user.phone_number}")
            else:
                return Response({
                    'message': 'Invalid verification method'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'message': f'Verification code sent successfully via {verification_method}',
                'method': verification_method
            }, status=status.HTTP_200_OK)
        except UserNotFoundException as e:
            logger.warning(f"Verification resend failed: {str(e)}. Email: {email}")
            return Response({
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Verification resend failed with unexpected error: {str(e)}", exc_info=True)
            return Response({
                'message': 'An unexpected error occurred. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

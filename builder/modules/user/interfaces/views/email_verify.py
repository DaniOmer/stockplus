"""
Email verification views for the user application.
This module contains the email verification views for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from datetime import datetime, timedelta

from builder.modules.user.application.services import UserService
from builder.modules.user.infrastructure.repositories import UserRepository
from builder.modules.user.infrastructure.repositories.token_repository import get_token_repository
from builder.modules.user.interfaces.serializers import EmailVerifySerializer, ResendVerificationEmailSerializer
from builder.modules import messenger
from builder.modules.user.domain.exceptions import (
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
        
        # Get the repositories
        user_service = UserService(UserRepository())
        token_repository = get_token_repository()
        
        try:
            # Verify the token
            token_data = token_repository.get_verification_token(token)
            if not token_data:
                raise TokenInvalidException("Invalid or expired token")
            
            # Get the user
            user_id = token_data['user_id']
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise UserNotFoundException(f"User with ID {user_id} not found")
            
            # Verify the user
            user_service.verify_user(user_id)
            
            # Delete the token
            token_repository.delete_verification_token(token)
            
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
        
        # Get the repositories
        user_service = UserService(UserRepository())
        token_repository = get_token_repository()
        
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
            code = user.generate_verification_token(method=verification_method)
            
            # Store the token
            expiry = datetime.now() + timedelta(hours=24)
            token_repository.store_verification_token(
                user_id=user.id,
                token=code,
                expiry=expiry,
                method=verification_method
            )
            
            # Send the verification code
            if verification_method == 'email':
                messenger.send_email(
                    target=user.email,
                    subject='Verify Your Email',
                    txt=f'Your verification code is: {code}',
                    html=f'<p>Your verification code is: <strong>{code}</strong></p>'
                )
            elif verification_method == 'sms':
                messenger.send_sms(
                    target=user.phone_number,
                    subject='Verify Your Account',
                    txt=f'Your verification code is: {code}'
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

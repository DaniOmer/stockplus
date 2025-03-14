"""
Token views for the user application.
This module contains the token views for the user application.
"""

import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from stockplus.modules.user.domain.entities import TokenType, TokenMethod
from stockplus.modules.user.infrastructure.repositories import TokenRepository
from stockplus.modules.user.application.services import UserService, TokenService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.interfaces.serializers.token import (
    TokenSerializer,
    CreateVerificationTokenSerializer,
    CreatePasswordResetTokenSerializer,
    CreateInvitationTokenSerializer,
    VerifyTokenSerializer
)
from stockplus.modules.user.domain.exceptions import (
    TokenInvalidException,
    TokenExpiredException
)
from stockplus.modules.messenger.infrastructure.utils import send_mail_message, send_sms_message

logger = logging.getLogger(__name__)

class TokenView(generics.GenericAPIView):
    """
    API endpoint for token operations.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        Get the serializer class based on the request method.
        """
        if self.request.method == 'GET':
            return TokenSerializer
        elif self.request.method == 'POST':
            action = self.request.query_params.get('action', 'verify')
            if action == 'create_verification':
                return CreateVerificationTokenSerializer
            elif action == 'create_password_reset':
                return CreatePasswordResetTokenSerializer
            elif action == 'create_invitation':
                return CreateInvitationTokenSerializer
            else:
                return VerifyTokenSerializer
        return TokenSerializer
    
    def get(self, request):
        """
        Get tokens for the authenticated user.
        
        Args:
            request: The request
            
        Returns:
            Response: The response containing the tokens
        """
        token_service = TokenService(TokenRepository())
        token_type = request.query_params.get('token_type')
        
        if token_type:
            try:
                token_type = TokenType(token_type)
            except ValueError:
                return Response({
                    'message': f"Invalid token type: {token_type}"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        tokens = token_service.get_tokens_by_user(request.user.id, token_type)
        serializer = self.get_serializer(tokens, many=True)
        
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create or verify a token.
        
        Args:
            request: The request
            
        Returns:
            Response: The response
        """
        action = request.query_params.get('action', 'verify')
        
        if action == 'create_verification':
            return self.create_verification_token(request)
        elif action == 'create_password_reset':
            return self.create_password_reset_token(request)
        elif action == 'create_invitation':
            return self.create_invitation_token(request)
        else:
            return self.verify_token(request)
    
    def create_verification_token(self, request):
        """
        Create a verification token.
        
        Args:
            request: The request
            
        Returns:
            Response: The response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_id = serializer.validated_data['user_id']
        method = serializer.validated_data.get('method', TokenMethod.EMAIL.value)
        
        # Check if the user exists
        user_service = UserService(UserRepository())
        user = user_service.get_user_by_id(user_id)
        
        if not user:
            return Response({
                'message': f"User with ID {user_id} not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Create the token
        token_service = TokenService()
        token = token_service.create_verification_token(user_id, TokenMethod(method))
        
        # Send the verification code
        if method == TokenMethod.EMAIL.value:
            if not user.email:
                return Response({
                    'message': 'User does not have an email address'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # Render the email template with the token
            from django.template.loader import render_to_string
            from django.urls import reverse
            from django.conf import settings
            
            verification_link = reverse('email-verify')
            verification_url = f"{settings.FRONTEND_URL}{verification_link}?token={token.token_value}"
            html_content = render_to_string('verification_email.html', {
                'user': user,
                'verification_url': verification_url,
                'token': token.token_value
            })
            
            send_mail_message(
                subject='Verify Your Email',
                target=user.email,
                template='verification_email.html',
                html=html_content,
                message=f'Your verification code is: {token.token_value}'
            )
            
            logger.info(f"Verification email sent to: {user.email}")
        elif method == TokenMethod.SMS.value:
            if not user.phone_number:
                return Response({
                    'message': 'User does not have a phone number'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            send_sms_message(
                to_phone=user.phone_number,
                message=f'Your verification code is: {token.token_value}'
            )
            
            logger.info(f"Verification SMS sent to: {user.phone_number}")
        
        # Return the token
        token_serializer = TokenSerializer(token)
        return Response(token_serializer.data, status=status.HTTP_201_CREATED)
    
    def create_password_reset_token(self, request):
        """
        Create a password reset token.
        
        Args:
            request: The request
            
        Returns:
            Response: The response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        # Check if the user exists
        user_service = UserService(UserRepository())
        user = user_service.get_user_by_email(email)
        
        if not user:
            # Don't reveal that the user doesn't exist
            logger.info(f"Password reset requested for non-existent account: {email}")
            return Response({
                'message': 'If your account exists, a password reset link has been sent'
            }, status=status.HTTP_200_OK)
        
        # Create the token
        token_service = TokenService()
        token = token_service.create_password_reset_token(user.id)
        
        # Send the password reset code
        from django.template.loader import render_to_string
        from django.urls import reverse
        from django.conf import settings
        
        reset_link = reverse('password-reset-confirm')
        reset_url = f"{settings.FRONTEND_URL}{reset_link}?token={token.token_value}"
        
        html_content = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
            'token': token.token_value
        })
        
        send_mail_message(
            subject='Reset Your Password',
            target=email,
            template='password_reset_email.html',
            html=html_content,
            message=f'Your password reset code is: {token.token_value}'
        )
        
        logger.info(f"Password reset email sent to: {email}")
        
        # Return a success message
        return Response({
            'message': 'If your account exists, a password reset link has been sent'
        }, status=status.HTTP_200_OK)
    
    def create_invitation_token(self, request):
        """
        Create an invitation token.
        
        Args:
            request: The request
            
        Returns:
            Response: The response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        # Create the token
        token_service = TokenService()
        token = token_service.create_invitation_token(request.user.id, email)
        
        # Send the invitation email
        from django.template.loader import render_to_string
        from django.urls import reverse
        from django.conf import settings
        
        invitation_link = reverse('register')
        invitation_url = f"{settings.FRONTEND_URL}{invitation_link}?token={token.token_value}"
        
        html_content = render_to_string('invitation_mail.html', {
            'invitation_url': invitation_url,
            'token': token.token_value
        })
        
        send_mail_message(
            subject='Invitation to Join',
            target=email,
            template='invitation_mail.html',
            html=html_content,
            message=f'You have been invited to join. Use this token to register: {token.token_value}'
        )
        
        logger.info(f"Invitation email sent to: {email}")
        
        # Return the token
        token_serializer = TokenSerializer(token)
        return Response(token_serializer.data, status=status.HTTP_201_CREATED)
    
    def verify_token(self, request):
        """
        Verify a token.
        
        Args:
            request: The request
            
        Returns:
            Response: The response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token_value = serializer.validated_data['token']
        token_type = TokenType(serializer.validated_data['token_type'])
        
        # Verify the token
        token_service = TokenService()
        
        try:
            token = token_service.verify_token(token_value, token_type)
            
            # Return the token
            token_serializer = TokenSerializer(token)
            return Response(token_serializer.data)
        except (TokenInvalidException, TokenExpiredException) as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Token verification failed with unexpected error: {str(e)}", exc_info=True)
            return Response({
                'message': 'An unexpected error occurred. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

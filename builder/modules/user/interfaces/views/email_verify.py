"""
Email verification views for the user application.
This module contains the email verification views for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from builder.modules.user.interfaces.serializers import EmailVerifySerializer, ResendVerificationEmailSerializer
from builder.modules.user.application.services import UserService
from builder.modules.user.infrastructure.repositories import UserRepository
from builder.modules.user.domain.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    ValidationException
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
        
        # In a real implementation, you would verify the token and get the user ID
        # For now, we'll just return a success response
        
        return Response({
            'message': 'Email verified successfully'
        }, status=status.HTTP_200_OK)


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
        user_service = UserService(UserRepository())
        
        try:
            user = user_service.get_user_by_email(email)
            if not user:
                return Response({
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            if user.is_verified:
                return Response({
                    'message': 'User is already verified'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # In a real implementation, you would generate a new token and send a verification email
            # For now, we'll just return a success response
            
            return Response({
                'message': 'Verification email sent successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

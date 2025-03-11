"""
Forgot password view for the user application.
This module contains the forgot password view for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from stockplus.modules.user.domain.exceptions import UserNotFoundException
from stockplus.modules.user.application.user_service import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository, TokenRepository
from stockplus.modules.messenger.infrastructure.utils import send_mail_message
from stockplus.modules.user.infrastructure.utils import get_password_reset_data_missive
from stockplus.modules.user.interfaces.serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer


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

        # Get the validated data
        email = serializer.validated_data.get('email')
        
        # Get user service
        user_repository = UserRepository()
        token_repository = TokenRepository()
        user_service = UserService(user_repository, token_repository)
        
        try:
            # Find the user
            user = user_service.get_user_by_email(email)
            if not user:
                # For security reasons, we don't want to reveal that the user doesn't exist
                return Response({
                    'message': 'If your account exists, a password reset code has been sent'
                }, status=status.HTTP_200_OK)
            
            # Generate a password reset token
            token = user_service.generate_password_reset_token(user.email, user.phone_number)
            
            # Send the password reset code
            data = get_password_reset_data_missive(user, token)
            send_mail_message(**data)
            
            return Response({
                'message': 'Password reset code sent successfully to your email',
            }, status=status.HTTP_200_OK)
        except UserNotFoundException as e:
            # For security reasons, we don't want to reveal that the user doesn't exist
            return Response({
                'message': 'If your account exists, a password reset code has been sent'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

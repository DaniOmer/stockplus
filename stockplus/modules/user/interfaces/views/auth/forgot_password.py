"""
Forgot password view for the user application.
This module contains the forgot password view for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from datetime import datetime, timedelta

from stockplus.modules.user.application.services import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.infrastructure.repositories.token_repository import get_token_repository
from stockplus.modules.user.interfaces.serializers import ForgotPasswordSerializer
from stockplus.modules.user.domain.exceptions import UserNotFoundException
from stockplus.modules import messenger


class ForgotPasswordView(generics.GenericAPIView):
    """
    API endpoint to request a password reset.
    """
    serializer_class = ForgotPasswordSerializer
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
        email_or_phone = serializer.validated_data.get('email_or_phone')
        verification_method = serializer.validated_data.get('verification_method', 'email')
        
        # Get the repositories
        user_service = UserService(UserRepository())
        token_repository = get_token_repository()
        
        try:
            # Find the user
            user = None
            if '@' in email_or_phone:
                user = user_service.get_user_by_email(email_or_phone)
            else:
                user = user_service.get_user_by_phone_number(email_or_phone)
            
            if not user:
                # For security reasons, we don't want to reveal that the user doesn't exist
                return Response({
                    'message': 'If your account exists, a password reset code has been sent'
                }, status=status.HTTP_200_OK)
            
            # Generate a random 6-digit code
            code = user.generate_password_reset_token(method=verification_method)
            
            # Store the code with an expiration time
            expiry = datetime.now() + timedelta(hours=1)
            token_repository.store_password_reset_token(
                user_id=user.id,
                token=code,
                expiry=expiry,
                method=verification_method
            )
            
            # Send the code to the user
            if verification_method == 'email' and user.email:
                # Send email with the code
                messenger.send_email(
                    target=user.email,
                    subject='Password Reset Code',
                    txt=f'Your password reset code is: {code}',
                    html=f'<p>Your password reset code is: <strong>{code}</strong></p>'
                )
            elif verification_method == 'sms' and user.phone_number:
                # Send SMS with the code
                messenger.send_sms(
                    target=user.phone_number,
                    subject='Password Reset',
                    txt=f'Your password reset code is: {code}'
                )
            else:
                return Response({
                    'message': 'Invalid verification method or contact information'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'message': 'Password reset code sent successfully',
                'user_id': user.id  # This will be used in the reset password endpoint
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

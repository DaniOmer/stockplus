"""
Reset password view for the user application.
This module contains the reset password view for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from stockplus.modules.user.application import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository, TokenRepository
from stockplus.modules.user.interfaces.serializers import PasswordResetConfirmSerializer
from stockplus.modules.user.domain.exceptions import (
    UserNotFoundException,
    TokenInvalidException,
    TokenExpiredException
)

class PasswordResetConfirmView(generics.GenericAPIView):
    """
    API endpoint to reset a user's password.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Reset a user's password.

        Args:
            request: The request

        Returns:
            Response: The response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the validated data
        code = serializer.validated_data.get('token')
        new_password = serializer.validated_data.get('new_password')
        
        # Get the repositories
        token_repository = TokenRepository()
        user_repository = UserRepository()
        user_service = UserService(user_repository, token_repository)
        
        try:
            # Reset the password
            user_service.reset_password(code, new_password)
            
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

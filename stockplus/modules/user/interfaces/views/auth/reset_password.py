"""
Reset password view for the user application.
This module contains the reset password view for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from stockplus.modules.user.application.services import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.infrastructure.repositories.token_repository import get_token_repository
from stockplus.modules.user.interfaces.serializers import ResetPasswordSerializer
from stockplus.modules.user.domain.exceptions import (
    UserNotFoundException,
    TokenInvalidException,
    TokenExpiredException
)


class ResetPasswordView(generics.GenericAPIView):
    """
    API endpoint to reset a user's password.
    """
    serializer_class = ResetPasswordSerializer
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
        user_id = serializer.validated_data.get('user_id')
        code = serializer.validated_data.get('code')
        new_password = serializer.validated_data.get('new_password')
        
        # Get the repositories
        user_service = UserService(UserRepository())
        token_repository = get_token_repository()
        
        try:
            # Get the user
            user = user_service.get_user_by_id(user_id)
            if not user:
                raise UserNotFoundException(f"User with ID {user_id} not found")
            
            # Verify the code
            token_data = token_repository.get_password_reset_token(code)
            if not token_data:
                raise TokenInvalidException("Invalid or expired code")
            
            if str(token_data['user_id']) != str(user_id):
                raise TokenInvalidException("Invalid code for this user")
            
            # Reset the password
            user_service.update_password(user_id, new_password)
            
            # Delete the token
            token_repository.delete_password_reset_token(code)
            
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

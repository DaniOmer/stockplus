"""
Password views for the user application.
"""
from rest_framework import generics
from rest_framework import status, permissions
from rest_framework.response import Response

from stockplus.modules.user.interfaces.serializers import PasswordUpdateSerializer
from stockplus.modules.user.application.user_service import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository, TokenRepository
from stockplus.modules.user.domain.exceptions import UserNotFoundException

class PasswordUpdateView(generics.GenericAPIView):
    """
    API endpoint for changing a user's password.
    """
    serializer_class = PasswordUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Change a user's password.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the user service
        user_repository = UserRepository()
        token_repository = TokenRepository()
        user_service = UserService(user_repository, token_repository)
        
        try:
            # Verify current password
            user = user_service.authenticate(
                email=request.user.email,
                password=serializer.validated_data['old_password']
            )
            
            if not user:
                return Response(
                    {'error': 'Old password is incorrect'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user_service.update_password(
                request.user.id,
                serializer.validated_data['new_password']
            )
            
            return Response(
                {'message': 'Password changed successfully'},
                status=status.HTTP_200_OK
            )
        except UserNotFoundException:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

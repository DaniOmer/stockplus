"""
Password views for the user application.
"""
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from stockplus.modules.user.interfaces.serializers.password import ChangePasswordSerializer
from stockplus.modules.user.application.user_service import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.domain.exceptions import UserNotFoundException


class ChangePasswordView(APIView):
    """
    API endpoint for changing a user's password.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Change a user's password.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        serializer = ChangePasswordSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_service = UserService(UserRepository())
        
        try:
            # Verify current password
            user = user_service.authenticate_user(
                email=request.user.email,
                password=serializer.validated_data['current_password']
            )
            
            if not user:
                return Response(
                    {'error': 'Current password is incorrect'},
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

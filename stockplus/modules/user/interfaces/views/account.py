"""
Account views for the user application.
"""

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from stockplus.modules.user.interfaces.serializers.user import UserSerializer
from stockplus.modules.user.application.user_service import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.domain.exceptions import UserNotFoundException

class AccountView(APIView):
    """
    API endpoint for retrieving user account information.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get the user's account information.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        user_service = UserService(UserRepository())
        
        try:
            user = user_service.get_user_by_id(request.user.id)
            
            if not user:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
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

"""
Authentication views for the user application.
This module contains the authentication views for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from stockplus.modules.user.application.user_service import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository, TokenRepository
from stockplus.modules.user.interfaces.serializers.user import UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    API endpoint to register a new user.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        """
        Add the user service to the serializer context.
        """
        context = super().get_serializer_context()
        user_repository = UserRepository()
        token_repository = TokenRepository()
        context['user_service'] = UserService(user_repository, token_repository)
        return context

    def create(self, request, *args, **kwargs):
        """
        Create a new user.

        Args:
            request: The request

        Returns:
            Response: The response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = serializer.save()
            return Response({
                'message': 'User registered successfully. Please check your email to verify your account.',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_verified': user.is_verified
                }
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
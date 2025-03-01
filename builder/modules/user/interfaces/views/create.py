"""
Create views for the user application.
This module contains the create views for the user application.
"""

from rest_framework import generics, permissions, serializers

from builder.modules.user.interfaces.serializers import UserSerializer
from builder.modules.user.application.services import UserService
from builder.modules.user.infrastructure.repositories import UserRepository


class UserCreateView(generics.CreateAPIView):
    """
    API endpoint to create a user.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_context(self):
        """
        Add the user service to the serializer context.
        
        Returns:
            dict: The serializer context
        """
        context = super().get_serializer_context()
        context['user_service'] = UserService(UserRepository())
        return context

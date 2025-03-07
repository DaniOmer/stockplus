"""
Detail views for the user application.
This module contains the detail views for the user application.
"""

from rest_framework import generics, permissions

from stockplus.modules.user.interfaces.serializers import UserProfileSerializer
from stockplus.modules.user.application.services import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve and update a user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Get the user object.
        
        Returns:
            User: The user object
        """
        user_service = UserService(UserRepository())
        return user_service.get_user_by_id(self.request.user.id)
    
    def get_serializer_context(self):
        """
        Add the user service to the serializer context.
        
        Returns:
            dict: The serializer context
        """
        context = super().get_serializer_context()
        context['user_service'] = UserService(UserRepository())
        return context

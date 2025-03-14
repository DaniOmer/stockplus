"""
User views for the user application.
This module contains the user views for the user application.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from stockplus.infrastructure.api.mixins import ResponseFormatterMixin
from stockplus.modules.user.application.services import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.interfaces.serializers import (
    UserBaseSerializer,
    UserUpdateSerializer,
    UserPasswordUpdateSerializer,
)

class UserViewSet(ResponseFormatterMixin, viewsets.ModelViewSet):
    """
    ViewSet for user management.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserBaseSerializer
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'update_password':
            return UserPasswordUpdateSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        """
        Return the current user's data.
        """
        user_repository = UserRepository()
        return user_repository.get_user_by_id(self.request.user.id)
        
    def update(self, request, *args, **kwargs):
        """
        Update user information.
        """
        serializer = self.get_serializer(data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        
        user_service = UserService(UserRepository())
        user = user_service.update_user(
            user_id=request.user.id,
            **serializer.validated_data
        )
        
        return self.format_response(
            data=UserBaseSerializer(user).data,
            message="User updated successfully",
            status=status.HTTP_200_OK
        )
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update user information.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
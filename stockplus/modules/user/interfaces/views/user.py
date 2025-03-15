"""
User views for the user application.
This module contains the user views for the user application.
"""

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from stockplus.infrastructure.api.mixins import ResponseFormatterMixin
from stockplus.modules.user.application.services import UserService, TokenService
from stockplus.modules.user.infrastructure.repositories import UserRepository, TokenRepository
from stockplus.modules.user.interfaces.serializers import (
    UserBaseSerializer,
    UserUpdateSerializer,
)

class UserViewSet(ResponseFormatterMixin, viewsets.ModelViewSet):
    """
    ViewSet for user management.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserBaseSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService(UserRepository(), TokenService(TokenRepository()))
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        """
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        """
        Return a queryset containing only the current user.
        This is required for ModelViewSet to work properly.
        """
        user = self.user_service.get_all_users()
        return user
    
    def list(self, request, *args, **kwargs):
        """
        Override list to return only the current user.
        """
        users = self.get_queryset()
        if not users:
            return self.format_response(
                message="User not found",
                status=status.HTTP_404_NOT_FOUND,
                success=False
            )
        
        serializer = self.get_serializer(users, many=True)
        return self.format_response(
            data=serializer.data,
            message="Users retrieved successfully",
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to ensure only the current user can be retrieved.
        """
        # Ensure the requested user is the current user
        if kwargs.get('pk') != 'me' and str(kwargs.get('pk')) != str(request.user.id):
            return self.format_response(
                message="You can only retrieve your own user data",
                status=status.HTTP_403_FORBIDDEN,
            )
        
        user = self.get_queryset().filter(id=request.user.id).first()
        if not user:
            return self.format_response(
                message="User not found",
                status=status.HTTP_404_NOT_FOUND,
            )
        
        serializer = self.get_serializer(user)
        return self.format_response(
            data=serializer.data,
            message="User retrieved successfully",
            status=status.HTTP_200_OK
        )
        
    def update(self, request, *args, **kwargs):
        """
        Update user information.
        """
        # Ensure the requested user is the current user
        if kwargs.get('pk') != 'me' and str(kwargs.get('pk')) != str(request.user.id):
            return self.format_response(
                message="You can only update your own user data",
                status=status.HTTP_403_FORBIDDEN,
            )
            
        # Get the current user instance
        instance = self.get_queryset().filter(id=request.user.id).first()
        if not instance:
            return self.format_response(
                message="User not found",
                status=status.HTTP_404_NOT_FOUND,
            )
        
        print("Request data ", request.data)
        # Create serializer with the instance and data
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=kwargs.get('partial', False)
        )
        serializer.is_valid(raise_exception=True)
        
        # Update the user using the service
        user = self.user_service.update_user(
            user_id=request.user.id,
            **serializer.validated_data
        )
        print("User updated successfully ", user)
        
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

"""
User views for the API.
This module contains the views for the User model.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from stockplus.config.dependencies import get_service
from stockplus.interfaces.api.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserProfileSerializer
)
from stockplus.domain.exceptions import (
    UserAlreadyExistsException,
    ResourceNotFoundException,
    ValidationException
)


class UserCreateAPIView(generics.CreateAPIView):
    """
    API endpoint for creating a new user.
    """
    
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """
        Create a new user.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_service = get_service('user_service')
        
        try:
            user = user_service.register_user(
                email=serializer.validated_data.get('email'),
                phone_number=serializer.validated_data.get('phone_number'),
                username=serializer.validated_data.get('username'),
                first_name=serializer.validated_data.get('first_name'),
                last_name=serializer.validated_data.get('last_name'),
                password=serializer.validated_data.get('password')
            )
            
            response_serializer = UserSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        except (UserAlreadyExistsException, ValidationException) as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating a user's profile.
    """
    
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """
        Get the user object.
        
        Returns:
            User: The user object
            
        Raises:
            ResourceNotFoundException: If the user is not found
        """
        user_service = get_service('user_service')
        user = user_service.get_user_by_id(self.kwargs['pk'])
        
        if not user:
            raise ResourceNotFoundException(f"User with ID {self.kwargs['pk']} not found")
        
        # Check permissions
        self.check_object_permissions(self.request, user)
        
        return user
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a user's profile.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """
        Update a user's profile.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        user = self.get_object()
        serializer = UserUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        user_service = get_service('user_service')
        
        try:
            updated_user = user_service.update_user_profile(
                user_id=user.id,
                first_name=serializer.validated_data.get('first_name'),
                last_name=serializer.validated_data.get('last_name'),
                date_of_birth=serializer.validated_data.get('date_of_birth')
            )
            
            response_serializer = UserProfileSerializer(updated_user)
            return Response(response_serializer.data)
        
        except ValidationException as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserVerifyAPIView(generics.GenericAPIView):
    """
    API endpoint for verifying a user's account.
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        Verify a user's account.
        
        Args:
            request: The HTTP request
            
        Returns:
            Response: The HTTP response
        """
        user_service = get_service('user_service')
        
        try:
            user = user_service.verify_user(request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
        except ResourceNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

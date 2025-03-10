"""
Profile views for the user application.
This module contains the profile views for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from stockplus.modules.user.application.user_service import UserService
from stockplus.modules.user.infrastructure.repositories import UserRepository
from stockplus.modules.user.interfaces.serializers.profile import UserProfileSerializer
from stockplus.modules.user.domain.exceptions import UserNotFoundException


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve and update a user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # For handling file uploads (avatar)
    
    def get_object(self):
        """
        Get the user object.
        
        Returns:
            User: The user object
        """
        return self.request.user
    
    def get_serializer_context(self):
        """
        Add the user service to the serializer context.
        
        Returns:
            dict: The serializer context
        """
        context = super().get_serializer_context()
        context['user_service'] = UserService(UserRepository())
        return context
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a user's profile.
        
        Args:
            request: The request
            
        Returns:
            Response: The response
        """
        user = self.get_object()
        serializer = self.get_serializer(user)
        
        return Response({
            'message': 'Profile retrieved successfully',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """
        Update a user's profile.
        
        Args:
            request: The request
            
        Returns:
            Response: The response
        """
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        try:
            serializer.is_valid(raise_exception=True)
            updated_user = serializer.save()
            
            return Response({
                'message': 'Profile updated successfully',
                'user': self.get_serializer(updated_user).data
            }, status=status.HTTP_200_OK)
        except UserNotFoundException as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

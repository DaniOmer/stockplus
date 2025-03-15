"""
Avatar views for the user module.
This module contains the views for avatar operations.
"""

import logging
import time
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from stockplus.infrastructure.api.mixins import ResponseFormatterMixin
from stockplus.modules.user.infrastructure.utils.hmac_validator import HMACValidator
from stockplus.modules.user.application.services import UserService, TokenService
from stockplus.modules.user.infrastructure.repositories import UserRepository, TokenRepository
from stockplus.modules.user.interfaces.serializers.avatar import (
    AvatarUploadSerializer,
    AvatarUrlSerializer,
    AvatarResponseSerializer,
)

logger = logging.getLogger(__name__)

class AvatarViewSet(ResponseFormatterMixin, viewsets.ViewSet):
    """
    ViewSet for avatar management.
    """
    serializer_class = AvatarUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService(UserRepository(), TokenService(TokenRepository()))

    @action(detail=False, methods=['post'], url_path='upload')
    def upload(self, request):
        """
        Upload a new avatar.
        """
        # Validate the request
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        # Upload the avatar
        user = self.user_service.upload_avatar(request.user, serializer.validated_data['avatar'])
        
        # Generate a URL for the avatar
        url_serializer = AvatarUrlSerializer(user)
        
        # Return the response
        response_data = {
            'avatar_url': url_serializer.data['url'],
            'message': 'Avatar uploaded successfully'
        }
        
        return self.format_response(
            data=response_data,
            message='Avatar uploaded successfully',
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['delete'], url_path='remove')
    def remove(self, request):
        """
        Remove the avatar.
        """
        # Get the user
        user = request.user
        
        # Check if the user has an avatar
        if not hasattr(user, 'avatar') or not user.avatar:
            return self.format_response(
                message='No avatar to remove',
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete the avatar
        user.avatar.delete(save=False)
        user.avatar = None
        user.save()
        
        # Return the response
        response_data = {
            'avatar_url': None,
            'message': 'Avatar removed successfully'
        }
        
        return self.format_response(
            data=response_data,
            message='Avatar removed successfully',
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='url')
    def get_url(self, request):
        """
        Get a signed URL for the avatar.
        """
        # Get the user
        user = request.user
        
        # Generate a URL for the avatar
        url_serializer = AvatarUrlSerializer(user)
        
        # Return the response
        return self.format_response(
            data=url_serializer.data,
            message='Avatar URL generated successfully',
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='signature')
    def get_signature(self, request):
        """
        Get an HMAC signature for secure upload.
        """
        # Generate a signature
        signature_data = HMACValidator.generate_signature(request.user.id)
        
        # Return the response
        return self.format_response(
            data=signature_data,
            message='Signature generated successfully',
            status=status.HTTP_200_OK
        )

"""
Avatar serializers for the user module.
This module contains the serializers for avatar operations.
"""

import time
from django.conf import settings
from rest_framework import serializers
from django.core.files.uploadedfile import UploadedFile

from stockplus.interface.serializer import BaseSerializer
from stockplus.modules.user.infrastructure.utils import HMACValidator, VirusScanner
from stockplus.modules.user.domain.exceptions import ValidationException

class AvatarUploadSerializer(BaseSerializer, serializers.Serializer):
    """
    Serializer for avatar upload.
    """
    avatar = serializers.ImageField(required=True)
    signature = serializers.CharField(required=True)
    timestamp = serializers.IntegerField(required=True)
    
    def validate(self, attrs):
        """
        Validate the avatar upload.
        """
        # Get the user
        user = self.context['request'].user
        
        # Validate the signature
        if not HMACValidator.validate_signature(
            user_id=user.id,
            signature=attrs['signature'],
            timestamp=attrs['timestamp']
        ):
            raise ValidationException("Invalid signature")
        
        # Get the avatar file
        avatar_file = attrs['avatar']
        
        # Check if the file is an image
        if not isinstance(avatar_file, UploadedFile):
            raise ValidationException("Invalid file")
        
        # Scan the file for viruses
        is_clean, message = VirusScanner.scan_file(avatar_file)
        if not is_clean:
            raise ValidationException(f"File rejected: {message}")
        
        return attrs

class AvatarUrlSerializer(BaseSerializer, serializers.Serializer):
    """
    Serializer for avatar URL.
    """
    url = serializers.CharField(read_only=True)
    expires_at = serializers.IntegerField(read_only=True)
    
    def to_representation(self, instance):
        """
        Generate a signed URL for the avatar.
        """
        # Get the user
        user = instance
        
        # Check if the user has an avatar
        if not user.avatar:
            return {
                'url': None,
                'expires_at': None
            }
        
        # Generate a signed URL for the avatar
        if settings.USE_S3:
            # For S3 storage, generate a pre-signed URL
            url = user.avatar.storage.url(
                user.avatar.name,
                parameters={'ResponseContentDisposition': 'inline'}
            )
            expires_at = int(time.time()) + settings.AWS_QUERYSTRING_EXPIRE
        else:
            # For local storage, just return the URL
            url = user.avatar.url
            expires_at = None
        
        return {
            'url': url,
            'expires_at': expires_at
        }

class AvatarResponseSerializer(BaseSerializer, serializers.Serializer):
    """
    Serializer for avatar response.
    """
    avatar_url = serializers.CharField(allow_null=True)
    message = serializers.CharField()

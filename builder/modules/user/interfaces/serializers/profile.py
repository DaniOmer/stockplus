"""
User profile serializers for the user application.
This module contains the user profile serializers for the user application.
"""

from rest_framework import serializers

from builder.modules.user.domain.models import User


class UserProfileSerializer(serializers.Serializer):
    """
    Serializer for the User profile.
    """
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    is_verified = serializers.BooleanField(read_only=True)
    company_id = serializers.IntegerField(read_only=True)
    role = serializers.CharField(read_only=True)
    
    def update(self, instance, validated_data):
        """
        Update a user's profile.
        
        Args:
            instance: The user instance
            validated_data: The validated data
            
        Returns:
            User: The updated user
        """
        user_service = self.context.get('user_service')
        if not user_service:
            raise ValueError('User service is required')
        
        # Update the user
        user = user_service.update_user(
            user_id=instance.id,
            email=validated_data.get('email', instance.email),
            phone_number=validated_data.get('phone_number', instance.phone_number),
            first_name=validated_data.get('first_name', instance.first_name),
            last_name=validated_data.get('last_name', instance.last_name)
        )
        
        return user

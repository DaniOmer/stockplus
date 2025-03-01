"""
User serializers for the user application.
This module contains the user serializers for the user application.
"""

from rest_framework import serializers

from builder.modules.user.domain.models import User


class UserSerializer(serializers.Serializer):
    """
    Serializer for the User model.
    """
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_verified = serializers.BooleanField(read_only=True)
    
    def create(self, validated_data):
        """
        Create a new user.
        
        Args:
            validated_data: The validated data
            
        Returns:
            User: The created user
        """
        user_service = self.context.get('user_service')
        if not user_service:
            raise ValueError('User service is required')
        
        # Create the user
        user = user_service.create_user(
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        
        return user
    
    def update(self, instance, validated_data):
        """
        Update a user.
        
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
        
        # Update the password if provided
        if 'password' in validated_data:
            user_service.update_password(user.id, validated_data['password'])
        
        return user

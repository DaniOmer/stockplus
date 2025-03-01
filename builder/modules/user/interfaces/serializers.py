"""
Serializers for the user application.
This module contains the serializers for the user application.
"""

from rest_framework import serializers

from builder.modules.user.domain.models import User, Invitation
from builder.modules.user.application.services import UserService, InvitationService
from builder.modules.user.domain.exceptions import (
    UserAlreadyExistsException,
    ValidationException
)


class UserSerializer(serializers.Serializer):
    """
    Serializer for the User model.
    """
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=False, allow_null=True)
    username = serializers.CharField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    first_name = serializers.CharField(required=False, allow_null=True)
    last_name = serializers.CharField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True, required=False)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    is_active = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    
    def create(self, validated_data):
        """
        Create a new user.
        
        Args:
            validated_data: The validated data
            
        Returns:
            User: The created user
            
        Raises:
            ValidationException: If the user data is invalid
            UserAlreadyExistsException: If a user with the given email or phone number already exists
        """
        user_service = self.context['user_service']
        
        try:
            user = user_service.register_user(
                email=validated_data.get('email'),
                phone_number=validated_data.get('phone_number'),
                username=validated_data.get('username'),
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                password=validated_data.get('password')
            )
            return user
        except (ValidationException, UserAlreadyExistsException) as e:
            raise serializers.ValidationError(str(e))
    
    def update(self, instance, validated_data):
        """
        Update a user.
        
        Args:
            instance: The user to update
            validated_data: The validated data
            
        Returns:
            User: The updated user
        """
        user_service = self.context['user_service']
        
        try:
            user = user_service.update_user_profile(
                user_id=instance.id,
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                username=validated_data.get('username'),
                date_of_birth=validated_data.get('date_of_birth')
            )
            return user
        except ValidationException as e:
            raise serializers.ValidationError(str(e))


class UserProfileSerializer(serializers.Serializer):
    """
    Serializer for the User profile.
    """
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(required=False, allow_null=True)
    phone_number = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=False, allow_null=True)
    last_name = serializers.CharField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True, required=False)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    is_active = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    
    def update(self, instance, validated_data):
        """
        Update a user's profile.
        
        Args:
            instance: The user to update
            validated_data: The validated data
            
        Returns:
            User: The updated user
        """
        user_service = self.context['user_service']
        
        try:
            user = user_service.update_user_profile(
                user_id=instance.id,
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                username=validated_data.get('username'),
                date_of_birth=validated_data.get('date_of_birth')
            )
            return user
        except ValidationException as e:
            raise serializers.ValidationError(str(e))


class InvitationSerializer(serializers.Serializer):
    """
    Serializer for the Invitation model.
    """
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    token = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """
        Create a new invitation.
        
        Args:
            validated_data: The validated data
            
        Returns:
            Invitation: The created invitation
            
        Raises:
            ValidationException: If the invitation data is invalid
            UserAlreadyExistsException: If a user with the given email already exists
        """
        invitation_service = self.context['invitation_service']
        sender_id = self.context['request'].user.id
        
        try:
            invitation = invitation_service.create_invitation(
                email=validated_data['email'],
                sender_id=sender_id
            )
            return invitation
        except (ValidationException, UserAlreadyExistsException) as e:
            raise serializers.ValidationError(str(e))


class EmailVerifySerializer(serializers.Serializer):
    """
    Serializer for email verification.
    """
    token = serializers.CharField()


class ResendVerificationEmailSerializer(serializers.Serializer):
    """
    Serializer for resending verification email.
    """
    email = serializers.EmailField()

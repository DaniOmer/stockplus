"""
Profile serializers for the user application.
"""
from rest_framework import serializers

from stockplus.modules.user.infrastructure.models.user_model import User


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the user profile.
    """
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone_number', 'first_name', 'last_name',
            'is_verified', 'company_id', 'role', 'avatar'
        ]
        read_only_fields = ['id', 'is_verified', 'company_id', 'role', 'avatar']
    
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
        
        # Update the avatar if provided
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
            instance.save()
        
        return user

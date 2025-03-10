"""
User serializers for the user application.
This module contains the user serializers for the user application.
"""

from rest_framework import serializers
from stockplus.modules.address.infrastructure.models import UserAddress

class UserSerializer(serializers.Serializer):
    """
    Serializer for the User model.
    """
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_verified = serializers.BooleanField(read_only=True)
    
    # Address fields
    country = serializers.CharField(required=True)
    
    def create(self, validated_data):
        """
        Create a new user.
        
        Args:
            validated_data: The validated data
            
        Returns:
            User: The created user
        """
        user_service = self.context.get('user_service')
        
        # Extract country data
        country = validated_data.pop('country', None)
        
        # Create the user domain entity
        created_user = user_service.create_user(
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        
        # Create user address if country is provided
        if country:
            UserAddress.objects.create(
                user=created_user,
                country=country
            )
        
        return created_user
    
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
        
        # Extract address data
        address_data = {
            'address': validated_data.pop('address', None),
            'complement': validated_data.pop('complement', None),
            'city': validated_data.pop('city', None),
            'postal_code': validated_data.pop('postal_code', None),
            'state': validated_data.pop('state', None),
            'country': validated_data.pop('country', None)
        }
        
        # Update the user domain entity
        user= user_service.update_user(
            user_id=instance.id,
            email=validated_data.get('email', instance.email),
            phone_number=validated_data.get('phone_number', instance.phone_number),
            first_name=validated_data.get('first_name', instance.first_name),
            last_name=validated_data.get('last_name', instance.last_name)
        )
        
        # Update the password if provided
        if 'password' in validated_data:
            user_service.update_password(user.id, validated_data['password'])
        
        # Update or create user address if country is provided
        if address_data['country']:
            user_address, created = UserAddress.objects.get_or_create(
                user=user,
                defaults={
                    'address': address_data['address'],
                    'complement': address_data['complement'],
                    'city': address_data['city'],
                    'postal_code': address_data['postal_code'],
                    'state': address_data['state'],
                    'country': address_data['country']
                }
            )
            
            if not created:
                # Update existing address
                if address_data['address'] is not None:
                    user_address.address = address_data['address']
                if address_data['complement'] is not None:
                    user_address.complement = address_data['complement']
                if address_data['city'] is not None:
                    user_address.city = address_data['city']
                if address_data['postal_code'] is not None:
                    user_address.postal_code = address_data['postal_code']
                if address_data['state'] is not None:
                    user_address.state = address_data['state']
                if address_data['country'] is not None:
                    user_address.country = address_data['country']
                user_address.save()
        
        return user

"""
Serializers for the address application.
This module contains the serializers for the address application.
"""

from rest_framework import serializers

from builder.models import UserAddress, CompanyAddress


class AddressSerializer(serializers.Serializer):
    """
    Base serializer for address entities.
    """
    id = serializers.IntegerField(read_only=True)
    address = serializers.CharField(required=True)
    complement = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    city = serializers.CharField(required=True)
    postal_code = serializers.CharField(required=True)
    state = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    state_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    country = serializers.CharField(required=True)
    country_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    cedex = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    cedex_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    special = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    index = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)


class UserAddressSerializer(AddressSerializer):
    """
    Serializer for user address entities.
    """
    user_id = serializers.IntegerField(required=True)
    is_default = serializers.BooleanField(required=False, default=False)
    
    def create(self, validated_data):
        """
        Create a new user address.
        
        Args:
            validated_data: The validated data
            
        Returns:
            UserAddress: The created user address
        """
        address_service = self.context.get('address_service')
        if not address_service:
            raise ValueError('Address service is required')
        
        # Create the address
        address = address_service.create_address(**validated_data)
        
        return address
    
    def update(self, instance, validated_data):
        """
        Update a user address.
        
        Args:
            instance: The user address instance
            validated_data: The validated data
            
        Returns:
            UserAddress: The updated user address
        """
        address_service = self.context.get('address_service')
        if not address_service:
            raise ValueError('Address service is required')
        
        # Update the address
        address = address_service.update_address(instance.id, **validated_data)
        
        return address


class CompanyAddressSerializer(AddressSerializer):
    """
    Serializer for company address entities.
    """
    company_id = serializers.IntegerField(required=True)
    
    def create(self, validated_data):
        """
        Create a new company address.
        
        Args:
            validated_data: The validated data
            
        Returns:
            CompanyAddress: The created company address
        """
        address_service = self.context.get('address_service')
        if not address_service:
            raise ValueError('Address service is required')
        
        # Create the address
        address = address_service.create_address(**validated_data)
        
        return address
    
    def update(self, instance, validated_data):
        """
        Update a company address.
        
        Args:
            instance: The company address instance
            validated_data: The validated data
            
        Returns:
            CompanyAddress: The updated company address
        """
        address_service = self.context.get('address_service')
        if not address_service:
            raise ValueError('Address service is required')
        
        # Update the address
        address = address_service.update_address(instance.id, **validated_data)
        
        return address


class UserAddressListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing user addresses.
    """
    
    class Meta:
        model = UserAddress
        fields = [
            'id', 'address', 'city', 'postal_code', 'country', 'is_default'
        ]


class CompanyAddressListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing company addresses.
    """
    
    class Meta:
        model = CompanyAddress
        fields = [
            'id', 'address', 'city', 'postal_code', 'country'
        ]

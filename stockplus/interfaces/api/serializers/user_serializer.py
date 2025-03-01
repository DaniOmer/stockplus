"""
User serializers for the API.
This module contains the serializers for the User model.
"""

from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """
    Serializer for the User model.
    """
    
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True, max_length=20)
    username = serializers.CharField(required=False, allow_null=True, max_length=100)
    first_name = serializers.CharField(required=False, allow_null=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_null=True, max_length=150)
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    is_verified = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    company_id = serializers.IntegerField(required=False, allow_null=True)
    role = serializers.CharField(required=False, allow_null=True, max_length=100)
    
    def validate(self, data):
        """
        Validate the data.
        
        Args:
            data: The data to validate
            
        Returns:
            dict: The validated data
            
        Raises:
            serializers.ValidationError: If the data is invalid
        """
        # Check that at least one of email or phone_number is provided
        if 'email' not in data and 'phone_number' not in data:
            raise serializers.ValidationError("Either email or phone number must be provided.")
        
        return data


class UserCreateSerializer(UserSerializer):
    """
    Serializer for creating a User.
    """
    
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})


class UserUpdateSerializer(UserSerializer):
    """
    Serializer for updating a User.
    """
    
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    username = serializers.CharField(required=False, allow_null=True, max_length=100)
    first_name = serializers.CharField(required=False, allow_null=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_null=True, max_length=150)
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    date_of_birth = serializers.DateField(required=False, allow_null=True)


class UserProfileSerializer(UserSerializer):
    """
    Serializer for the User profile.
    """
    
    fullname = serializers.CharField(read_only=True)

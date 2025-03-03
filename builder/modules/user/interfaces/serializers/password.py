"""
Password serializers for the user application.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    """
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        """
        Validate the password change data.
        
        Args:
            data: The data to validate
            
        Returns:
            dict: The validated data
            
        Raises:
            serializers.ValidationError: If the data is invalid
        """
        # Check if new password and confirm password match
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password do not match.")
        
        # Validate the new password
        try:
            validate_password(data['new_password'])
        except Exception as e:
            raise serializers.ValidationError(str(e))
        
        return data

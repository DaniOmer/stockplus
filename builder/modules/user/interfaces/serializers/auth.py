"""
Authentication serializers for the user application.
This module contains the authentication serializers for the user application.
"""

from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email_or_phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for forgot password.
    """
    email_or_phone = serializers.CharField(required=True)
    verification_method = serializers.ChoiceField(
        choices=['email', 'sms'],
        default='email',
        required=False
    )


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for reset password.
    """
    user_id = serializers.IntegerField(required=True)
    code = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate_new_password(self, value):
        """
        Validate the new password.
        
        Args:
            value: The password
            
        Returns:
            str: The validated password
        """
        # Add password validation logic here
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        return value


class EmailVerifySerializer(serializers.Serializer):
    """
    Serializer for email verification.
    """
    token = serializers.CharField(required=True)


class ResendVerificationEmailSerializer(serializers.Serializer):
    """
    Serializer for resending verification email.
    """
    email = serializers.EmailField(required=True)
    verification_method = serializers.ChoiceField(
        choices=['email', 'sms'],
        default='email',
        required=False
    )

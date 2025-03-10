"""
Authentication serializers for the user application.
This module contains the authentication serializers for the user application.
"""

from rest_framework import serializers


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
    verification_method = serializers.ChoiceField(choices=['email', 'sms'], default='email', required=False)


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    
    Password reset is only available via email.
    """
    email = serializers.EmailField(required=True)

    def validate(self, data):
        """
        Validate that email is provided.
        """
        if not data.get('email'):
            raise serializers.ValidationError("Email is required for password reset")
        
        return data


class PasswordResetVerifySerializer(serializers.Serializer):
    """
    Serializer for password reset verification.
    """
    token = serializers.CharField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation.
    """
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        """
        Validate that the passwords match.
        """
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate(self, data):
        """
        Validate that either email or phone_number is provided.
        """
        if not data.get('email') and not data.get('phone_number'):
            raise serializers.ValidationError("Either email or phone_number must be provided")
        return data


# Aliases for backward compatibility
ForgotPasswordSerializer = PasswordResetRequestSerializer
ResetPasswordSerializer = PasswordResetConfirmSerializer

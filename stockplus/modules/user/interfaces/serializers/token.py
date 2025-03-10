"""
Token serializers for the user application.
This module contains the token serializers for the user application.
"""

from rest_framework import serializers

from stockplus.modules.user.domain.entities import TokenType, TokenMethod


class TokenSerializer(serializers.Serializer):
    """
    Serializer for tokens.
    """
    id = serializers.UUIDField(read_only=True)
    token_value = serializers.CharField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    token_type = serializers.ChoiceField(
        choices=[(t.value, t.name) for t in TokenType],
        read_only=True
    )
    method = serializers.ChoiceField(
        choices=[(m.value, m.name) for m in TokenMethod],
        read_only=True
    )
    expiry = serializers.DateTimeField(read_only=True)
    is_used = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True, allow_null=True)


class CreateVerificationTokenSerializer(serializers.Serializer):
    """
    Serializer for creating verification tokens.
    """
    user_id = serializers.UUIDField(required=True)
    method = serializers.ChoiceField(
        choices=[(m.value, m.name) for m in TokenMethod],
        default=TokenMethod.EMAIL.value
    )


class CreatePasswordResetTokenSerializer(serializers.Serializer):
    """
    Serializer for creating password reset tokens.
    """
    email = serializers.EmailField(required=True)


class CreateInvitationTokenSerializer(serializers.Serializer):
    """
    Serializer for creating invitation tokens.
    """
    email = serializers.EmailField(required=True)


class VerifyTokenSerializer(serializers.Serializer):
    """
    Serializer for verifying tokens.
    """
    token = serializers.CharField(required=True)
    token_type = serializers.ChoiceField(
        choices=[(t.value, t.name) for t in TokenType],
        required=True
    )

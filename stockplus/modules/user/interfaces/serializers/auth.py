"""
Authentication serializers for the user application.
This module contains the authentication serializers for the user application.
"""

from pydantic import ValidationError as PydanticValidationError

from rest_framework import serializers
from stockplus.modules.user.domain.exceptions import ValidationException
from stockplus.modules.user.infrastructure.dtos import (
    EmailVerifyDTO,
    ResendVerificationEmailDTO,
    PasswordResetRequestDTO,
    PasswordResetConfirmDTO,
    PasswordUpdateDTO,
    UserLoginDTO,
)

class EmailVerifySerializer(serializers.Serializer):
    """
    Serializer for email verification.
    """
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            return EmailVerifyDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException(e.errors()[0]['msg'], errors=e.errors())

class ResendVerificationEmailSerializer(serializers.Serializer):
    """
    Serializer for resending verification email.
    """
    email = serializers.EmailField(required=True)
    verification_method = serializers.ChoiceField(choices=['email', 'sms'], default='email', required=False)

    def validate(self, attrs):
        try:
            return ResendVerificationEmailDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException(e.errors()[0]['msg'], errors=e.errors())

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    """
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        try:
            return PasswordResetRequestDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException(e.errors()[0]['msg'], errors=e.errors())

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation.
    """
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            return PasswordResetConfirmDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException(e.errors()[0]['msg'], errors=e.errors())

class PasswordUpdateSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            return PasswordUpdateDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException(e.errors()[0]['msg'], errors=e.errors())

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            return UserLoginDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException(e.errors()[0]['msg'], errors=e.errors())

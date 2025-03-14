"""
User serializers for the user application.
This module contains the user serializers for the user application.
"""

from pydantic import ValidationError as PydanticValidationError

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from stockplus.interface.serializer import BaseSerializer
from stockplus.modules.user.domain.exceptions import ValidationException
from stockplus.modules.user.infrastructure.models import User
from stockplus.modules.user.infrastructure.dtos import (
    UserCreateDTO,
    UserUpdateDTO,
    UserPasswordUpdateDTO,
)

class UserBaseSerializer(BaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone_number', 'first_name', 
            'last_name', 'is_verified', 'is_active'
        ]
        read_only_fields = ['id', 'is_verified', 'is_active']
    
    def is_valid(self, raise_exception=False):
        try:
            return super().is_valid(raise_exception=True)
        except ValidationError as exc:
            raise ValidationException(
                message="Validation failed.",
                errors=exc
            )

class UserCreateSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + ['password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        try:
            return UserCreateDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException(e.errors()[0]['msg'], errors=e.errors())
        except Exception as e:
            raise ValidationException(str(e))

class UserUpdateSerializer(UserBaseSerializer):
    def validate(self, attrs):
        try:
            return UserUpdateDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException("Could not validate user data", errors=e.errors())

class UserPasswordUpdateSerializer(serializers.Serializer):
    def validate(self, attrs):
        try:
            return UserPasswordUpdateDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException("Could not validate password data", errors=e.errors())

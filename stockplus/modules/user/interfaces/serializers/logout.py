"""
Logout serializer for the user application.
This module contains the logout serializer for the user application.
"""

from pydantic import ValidationError as PydanticValidationError

from rest_framework import serializers
from stockplus.modules.user.domain.exceptions import ValidationException
from stockplus.modules.user.infrastructure.dtos.logout_dto import LogoutDTO

class LogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout.
    """
    refresh_token = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            return LogoutDTO(**attrs).model_dump(exclude_none=True)
        except PydanticValidationError as e:
            raise ValidationException(e.errors()[0]['msg'], errors=e.errors())

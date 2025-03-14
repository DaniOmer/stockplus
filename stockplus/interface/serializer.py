from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from stockplus.domain.exceptions import DomainException

class BaseSerializer(serializers.Serializer):
    def is_valid(self, raise_exception=False):
        try:
            return super().is_valid(raise_exception=True)
        except ValidationError as exc:
            raise DomainException(
                message="Validation failed.", errors=exc)
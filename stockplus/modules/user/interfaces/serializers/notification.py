"""
Notification serializers for the user application.
"""

from rest_framework import serializers

class NotificationSerializer(serializers.Serializer):
    """
    Serializer for notification objects.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField()
    message = serializers.CharField()
    type = serializers.CharField()
    read = serializers.BooleanField()
    link = serializers.URLField(allow_null=True, required=False)
    date_create = serializers.DateTimeField(read_only=True)
    date_update = serializers.DateTimeField(read_only=True)


class NotificationListSerializer(serializers.Serializer):
    """
    Serializer for listing notification objects.
    """
    title = serializers.CharField()
    message = serializers.CharField()
    type = serializers.CharField()
    read = serializers.BooleanField()
    link = serializers.URLField(allow_null=True, required=False)
    date_create = serializers.DateTimeField(read_only=True)


class NotificationCreateSerializer(serializers.Serializer):
    """
    Serializer for creating notification objects.
    """
    title = serializers.CharField()
    message = serializers.CharField()
    type = serializers.CharField()
    link = serializers.URLField(allow_null=True, required=False)

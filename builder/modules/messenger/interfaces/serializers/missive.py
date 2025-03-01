"""
Serializers for the messenger application.
"""
from rest_framework import serializers


class MissiveSerializer(serializers.Serializer):
    """Serializer for missive objects."""
    
    id = serializers.IntegerField(read_only=True)
    mode = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    target = serializers.CharField()
    subject = serializers.CharField()
    html = serializers.CharField(required=False)
    txt = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        fields = [
            'id', 'mode', 'status', 'target', 'subject', 
            'html', 'txt', 'created_at', 'updated_at'
        ]


class EmailMissiveSerializer(serializers.Serializer):
    """Serializer for creating email missives."""
    
    to_email = serializers.EmailField()
    subject = serializers.CharField()
    message = serializers.CharField()
    html_message = serializers.CharField(required=False)
    
    class Meta:
        fields = ['to_email', 'subject', 'message', 'html_message']


class SMSMissiveSerializer(serializers.Serializer):
    """Serializer for creating SMS missives."""
    
    to_phone = serializers.CharField()
    message = serializers.CharField()
    
    class Meta:
        fields = ['to_phone', 'message']

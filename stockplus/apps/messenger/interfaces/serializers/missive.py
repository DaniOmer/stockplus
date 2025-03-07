"""
Serializers for the messenger application.
This module contains the serializers for the messenger application.
"""

from rest_framework import serializers

from stockplus.modules.messenger import choices
from stockplus.modules.messenger.domain.entities.missive import Missive

class MissiveSerializer(serializers.ModelSerializer):
    """
    Serializer for missive entities.
    """
    
    class Meta:
        model = Missive
        fields = [
            'id', 'mode', 'status', 'target', 'subject', 
            'html', 'txt', 'date_create', 'date_update'
        ]
        read_only_fields = ['id', 'date_create', 'date_update']


class MissiveListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing missives.
    """
    
    class Meta:
        model = Missive
        fields = [
            'id', 'mode', 'status', 'target', 'subject', 'date_create'
        ]


class EmailMissiveSerializer(serializers.Serializer):
    """
    Serializer for creating email missives.
    """
    to_email = serializers.EmailField(required=True)
    subject = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    html_message = serializers.CharField(required=False, allow_blank=True)
    
    def create(self, validated_data):
        """
        Create a new email missive.
        
        Args:
            validated_data: The validated data
            
        Returns:
            Missive: The created missive
        """
        messenger_service = self.context.get('messenger_service')
        if not messenger_service:
            raise ValueError('Messenger service is required')
        
        to_email = validated_data.pop('to_email')
        subject = validated_data.pop('subject')
        message = validated_data.pop('message')
        html_message = validated_data.pop('html_message', None)
        
        # Create the missive
        missive = messenger_service.create_email_missive(
            to_email=to_email,
            subject=subject,
            message=message,
            html_message=html_message,
            **validated_data
        )
        
        return missive


class SMSMissiveSerializer(serializers.Serializer):
    """
    Serializer for creating SMS missives.
    """
    to_phone = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    
    def create(self, validated_data):
        """
        Create a new SMS missive.
        
        Args:
            validated_data: The validated data
            
        Returns:
            Missive: The created missive
        """
        messenger_service = self.context.get('messenger_service')
        if not messenger_service:
            raise ValueError('Messenger service is required')
        
        to_phone = validated_data.pop('to_phone')
        message = validated_data.pop('message')
        
        # Create the missive
        missive = messenger_service.create_sms_missive(
            to_phone=to_phone,
            message=message,
            **validated_data
        )
        
        return missive


class MissiveStatusSerializer(serializers.Serializer):
    """
    Serializer for missive status.
    """
    status = serializers.ChoiceField(choices=choices.STATUS)
    
    def update(self, instance, validated_data):
        """
        Update the missive status.
        
        Args:
            instance: The missive instance
            validated_data: The validated data
            
        Returns:
            Missive: The updated missive
        """
        status = validated_data.get('status')
        
        if status == choices.STATUS_PREPARE:
            instance.prepare()
        elif status == choices.STATUS_SENT:
            instance.to_sent()
        elif status == choices.STATUS_ERROR:
            instance.to_error()
        
        instance.save()
        return instance

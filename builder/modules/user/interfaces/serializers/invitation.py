"""
Invitation serializers for the user application.
This module contains the invitation serializers for the user application.
"""

from rest_framework import serializers

from builder.modules.user.domain.models import Invitation
from builder.modules.user.domain.exceptions import (
    UserAlreadyExistsException,
    ValidationException
)


class InvitationSerializer(serializers.Serializer):
    """
    Serializer for the Invitation model.
    """
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True)
    token = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """
        Create a new invitation.
        
        Args:
            validated_data: The validated data
            
        Returns:
            Invitation: The created invitation
        """
        invitation_service = self.context.get('invitation_service')
        if not invitation_service:
            raise ValueError('Invitation service is required')
        
        # Get the sender ID from the request
        sender_id = self.context['request'].user.id
        
        try:
            # Create the invitation
            invitation = invitation_service.create_invitation(
                email=validated_data.get('email'),
                sender_id=sender_id
            )
            
            return invitation
        except UserAlreadyExistsException as e:
            raise serializers.ValidationError(str(e))
        except ValidationException as e:
            raise serializers.ValidationError(str(e))

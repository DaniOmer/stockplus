"""
Invitation views for the user application.
This module contains the invitation views for the user application.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from builder.modules.user.interfaces.serializers import InvitationSerializer
from builder.modules.user.application.services import InvitationService
from builder.modules.user.infrastructure.repositories import InvitationRepository, UserRepository
from builder.modules.user.domain.exceptions import (
    InvitationNotFoundException,
    InvitationExpiredException,
    InvitationAlreadyValidatedException,
)


class InvitationCreateView(generics.CreateAPIView):
    """
    API endpoint to create an invitation.
    """
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        """
        Add the invitation service to the serializer context.
        
        Returns:
            dict: The serializer context
        """
        context = super().get_serializer_context()
        context['invitation_service'] = InvitationService(
            InvitationRepository(),
            UserRepository()
        )
        return context


class InvitationValidateView(generics.GenericAPIView):
    """
    API endpoint to validate an invitation.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, token):
        """
        Validate an invitation.
        
        Args:
            request: The request
            token: The invitation token
            
        Returns:
            Response: The response
        """
        invitation_service = InvitationService(
            InvitationRepository(),
            UserRepository()
        )
        
        try:
            invitation = invitation_service.validate_invitation(token)
            return Response({
                'message': 'Invitation validated successfully',
                'email': invitation.email
            }, status=status.HTTP_200_OK)
        except InvitationNotFoundException:
            return Response({
                'message': 'Invitation not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except InvitationExpiredException:
            return Response({
                'message': 'Invitation has expired'
            }, status=status.HTTP_400_BAD_REQUEST)
        except InvitationAlreadyValidatedException:
            return Response({
                'message': 'Invitation has already been validated'
            }, status=status.HTTP_400_BAD_REQUEST)

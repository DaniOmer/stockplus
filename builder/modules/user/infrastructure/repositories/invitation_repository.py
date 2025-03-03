"""
Invitation repository implementation.
This module contains the invitation repository implementation.
"""

import uuid
import datetime
from typing import List, Optional
from django.utils import timezone

from builder.modules.user.infrastructure.models import Invitation
from builder.modules.user.application.interfaces import InvitationRepositoryInterface


class InvitationRepository(InvitationRepositoryInterface):
    """
    Invitation repository implementation.

    This class implements the InvitationRepositoryInterface using Django ORM.
    """

    def get_by_id(self, invitation_id) -> Optional[Invitation]:
        """
        Get an invitation by ID.

        Args:
            invitation_id: The ID of the invitation to retrieve

        Returns:
            Invitation: The invitation with the given ID or None if not found
        """
        try:
            return Invitation.objects.get(id=invitation_id)
        except Invitation.DoesNotExist:
            return None

    def get_by_email(self, email) -> Optional[Invitation]:
        """
        Get an invitation by email.

        Args:
            email: The email of the invitation to retrieve

        Returns:
            Invitation: The invitation with the given email or None if not found
        """
        try:
            return Invitation.objects.get(email=email)
        except Invitation.DoesNotExist:
            return None

    def get_by_token(self, token) -> Optional[Invitation]:
        """
        Get an invitation by token.

        Args:
            token: The token of the invitation to retrieve

        Returns:
            Invitation: The invitation with the given token or None if not found
        """
        try:
            return Invitation.objects.get(token=token)
        except Invitation.DoesNotExist:
            return None

    def get_by_sender_id(self, sender_id) -> List[Invitation]:
        """
        Get all invitations sent by a user.

        Args:
            sender_id: The ID of the sender

        Returns:
            List[Invitation]: A list of invitations sent by the user
        """
        return list(Invitation.objects.filter(sender_id=sender_id))

    def save(self, invitation: Invitation) -> Invitation:
        """
        Save an invitation.

        Args:
            invitation: The invitation to save

        Returns:
            Invitation: The saved invitation
        """
        # If the invitation is new, generate a token and set expiry date
        if not invitation.id:
            invitation.token = str(uuid.uuid4())
            invitation.expires_at = timezone.now() + datetime.timedelta(days=7)
            invitation.status = 'PENDING'

        invitation.save()
        return invitation

    def delete(self, invitation_id) -> bool:
        """
        Delete an invitation.

        Args:
            invitation_id: The ID of the invitation to delete

        Returns:
            bool: True if the invitation was deleted, False otherwise
        """
        try:
            invitation = Invitation.objects.get(id=invitation_id)
            invitation.delete()
            return True
        except Invitation.DoesNotExist:
            return False
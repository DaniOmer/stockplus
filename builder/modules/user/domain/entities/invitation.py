"""
Domain entities for the user application.
This module contains the domain models for the invitation.
"""

import uuid
from datetime import datetime, timedelta

class Invitation:
    """
    Invitation domain model.
    """

    def __init__(self, id=None, email=None, token=None, sender_id=None,
                 status='PENDING', expires_at=None, created_at=None, updated_at=None):
        """
        Initialize a new Invitation instance.

        Args:
            id: The invitation's ID
            email: The email of the invitee
            token: The invitation token
            sender_id: The ID of the sender
            status: The invitation status
            expires_at: When the invitation expires
            created_at: When the invitation was created
            updated_at: When the invitation was last updated
        """
        self.id = id
        self.email = email
        self.token = token or str(uuid.uuid4())
        self.sender_id = sender_id
        self.status = status
        self.expires_at = expires_at or (datetime.now() + timedelta(days=7))
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def is_valid(self):
        """
        Check if the invitation is valid.

        Returns:
            bool: Whether the invitation is valid
        """
        return self.status == 'PENDING' and self.expires_at > datetime.now()

    def mark_as_validated(self):
        """
        Mark the invitation as validated.
        """
        self.status = 'VALIDATED'
        self.updated_at = datetime.now()

    def mark_as_expired(self):
        """
        Mark the invitation as expired.
        """
        self.status = 'EXPIRED'
        self.updated_at = datetime.now()

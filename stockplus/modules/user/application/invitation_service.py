"""
Invitation service for the user application.
This module contains the invitation service for the user application.
"""

import logging
import secrets
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from stockplus.modules.user.domain.entities.invitation import Invitation
from stockplus.modules.user.application.interfaces import InvitationRepositoryInterface
from stockplus.modules.user.domain.exceptions import (
    InvitationNotFoundException,
    InvitationExpiredException,
    InvitationAlreadyValidatedException,
    ValidationException,
)

logger = logging.getLogger(__name__)


class InvitationService:
    """
    Invitation service.
    
    This class implements the application logic for invitations. It uses the invitation repository
    to access and manipulate invitation data and enforces business rules.
    """
    
    def __init__(self, invitation_repository: InvitationRepositoryInterface):
        """
        Initialize a new InvitationService instance.
        
        Args:
            invitation_repository: The invitation repository to use
        """
        self.invitation_repository = invitation_repository
    
    def get_invitation_by_id(self, invitation_id) -> Optional[Invitation]:
        """
        Get an invitation by ID.
        
        Args:
            invitation_id: The ID of the invitation to retrieve
            
        Returns:
            Invitation: The invitation with the given ID or None if not found
        """
        return self.invitation_repository.get_by_id(invitation_id)
    
    def get_invitation_by_token(self, token) -> Optional[Invitation]:
        """
        Get an invitation by token.
        
        Args:
            token: The token of the invitation to retrieve
            
        Returns:
            Invitation: The invitation with the given token or None if not found
        """
        return self.invitation_repository.get_by_token(token)
    
    def get_invitation_by_email(self, email) -> Optional[Invitation]:
        """
        Get an invitation by email.
        
        Args:
            email: The email of the invitation to retrieve
            
        Returns:
            Invitation: The invitation with the given email or None if not found
        """
        return self.invitation_repository.get_by_email(email)
    
    def get_invitations_by_company_id(self, company_id) -> List[Invitation]:
        """
        Get all invitations for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            List[Invitation]: A list of invitations for the company
        """
        return self.invitation_repository.get_by_company_id(company_id)
    
    def create_invitation(self, sender_id, email, company_id, role, expiry_days=7) -> Invitation:
        """
        Create a new invitation.
        
        Args:
            sender_id: The ID of the user sending the invitation
            email: The email of the user to invite
            company_id: The ID of the company to invite the user to
            role: The role to assign to the user
            expiry_days: The number of days until the invitation expires
            
        Returns:
            Invitation: The created invitation
            
        Raises:
            ValidationException: If the email is invalid or already invited
        """
        # Check if the email is already invited
        existing_invitation = self.invitation_repository.get_by_email(email)
        if existing_invitation:
            raise ValidationException(f"An invitation for {email} already exists")
        
        # Generate a token
        token = ''.join(secrets.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(32))
        
        # Set the expiry date
        expiry = datetime.now() + timedelta(days=expiry_days)
        
        # Create the invitation
        invitation = Invitation(
            sender_id=sender_id,
            email=email,
            company_id=company_id,
            role=role,
            token=token,
            expiry=expiry,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Save the invitation
        return self.invitation_repository.save(invitation)
    
    def validate_invitation(self, token) -> Invitation:
        """
        Validate an invitation.
        
        Args:
            token: The token of the invitation to validate
            
        Returns:
            Invitation: The validated invitation
            
        Raises:
            InvitationNotFoundException: If the invitation is not found
            InvitationExpiredException: If the invitation has expired
        """
        # Get the invitation
        invitation = self.invitation_repository.get_by_token(token)
        if not invitation:
            raise InvitationNotFoundException(f"Invitation with token {token} not found")
        
        # Check if the invitation has expired
        if invitation.expiry < datetime.now():
            raise InvitationExpiredException(f"Invitation with token {token} has expired")
        
        return invitation
    
    def delete_invitation(self, invitation_id) -> bool:
        """
        Delete an invitation.
        
        Args:
            invitation_id: The ID of the invitation to delete
            
        Returns:
            bool: True if the invitation was deleted, False otherwise
            
        Raises:
            InvitationNotFoundException: If the invitation is not found
        """
        # Check if the invitation exists
        invitation = self.invitation_repository.get_by_id(invitation_id)
        if not invitation:
            raise InvitationNotFoundException(f"Invitation with ID {invitation_id} not found")
        
        # Delete the invitation
        return self.invitation_repository.delete(invitation_id)

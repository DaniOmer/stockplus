"""
Application interfaces for the user application.
This module contains the application interfaces for the user application.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from stockplus.modules.user.domain.entities import Invitation

class IInvitationRepository(ABC):
    """
    Invitation repository interface.
    
    This interface defines the methods that an invitation repository must implement.
    """
    
    @abstractmethod
    def get_by_id(self, invitation_id) -> Optional[Invitation]:
        """
        Get an invitation by ID.
        
        Args:
            invitation_id: The ID of the invitation to retrieve
            
        Returns:
            Invitation: The invitation with the given ID or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_email(self, email) -> Optional[Invitation]:
        """
        Get an invitation by email.
        
        Args:
            email: The email of the invitation to retrieve
            
        Returns:
            Invitation: The invitation with the given email or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_token(self, token) -> Optional[Invitation]:
        """
        Get an invitation by token.
        
        Args:
            token: The token of the invitation to retrieve
            
        Returns:
            Invitation: The invitation with the given token or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_sender_id(self, sender_id) -> List[Invitation]:
        """
        Get all invitations sent by a user.
        
        Args:
            sender_id: The ID of the sender
            
        Returns:
            List[Invitation]: A list of invitations sent by the user
        """
        pass
    
    @abstractmethod
    def save(self, invitation: Invitation) -> Invitation:
        """
        Save an invitation.
        
        Args:
            invitation: The invitation to save
            
        Returns:
            Invitation: The saved invitation
        """
        pass
    
    @abstractmethod
    def delete(self, invitation_id) -> bool:
        """
        Delete an invitation.
        
        Args:
            invitation_id: The ID of the invitation to delete
            
        Returns:
            bool: True if the invitation was deleted, False otherwise
        """
        pass
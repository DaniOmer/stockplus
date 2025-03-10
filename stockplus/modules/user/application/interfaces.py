"""
Application interfaces for the user application.
This module contains the application interfaces for the user application.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from stockplus.modules.user.domain.entities import User, Token, Invitation, Notification, NotificationType


class UserRepositoryInterface(ABC):
    """
    User repository interface.
    
    This interface defines the methods that a user repository must implement.
    """
    
    @abstractmethod
    def get_by_id(self, user_id) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            User: The user with the given ID or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_email(self, email) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            email: The email of the user to retrieve
            
        Returns:
            User: The user with the given email or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_phone_number(self, phone_number) -> Optional[User]:
        """
        Get a user by phone number.
        
        Args:
            phone_number: The phone number of the user to retrieve
            
        Returns:
            User: The user with the given phone number or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_company_id(self, company_id) -> List[User]:
        """
        Get all users for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            List[User]: A list of users for the company
        """
        pass
    
    @abstractmethod
    def save(self, user: User) -> User:
        """
        Save a user.
        
        Args:
            user: The user to save
            
        Returns:
            User: The saved user
        """
        pass
    
    @abstractmethod
    def update_password(self, user_id, new_password) -> User:
        """
        Update a user's password.
        
        Args:
            user_id: The ID of the user to update
            new_password: The new password
            
        Returns:
            User: The updated user
        """
        pass
    
    @abstractmethod
    def verify_password(self, user_id, password) -> bool:
        """
        Verify a user's password.
        
        Args:
            user_id: The ID of the user
            password: The password to verify
            
        Returns:
            bool: True if the password is correct, False otherwise
        """
        pass
    
    @abstractmethod
    def delete(self, user_id) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: The ID of the user to delete
            
        Returns:
            bool: True if the user was deleted, False otherwise
        """
        pass


class ITokenRepository(ABC):
    """
    Token repository interface.
    
    This interface defines the methods that a token repository must implement.
    """
    
    @abstractmethod
    def get_by_value(self, token_value) -> Optional[Token]:
        """
        Get a token by value.
        
        Args:
            token_value: The value of the token to retrieve
            
        Returns:
            Token: The token with the given value or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_user_and_type(self, user_id, token_type) -> List[Token]:
        """
        Get all tokens for a user with a given type.
        
        Args:
            user_id: The ID of the user
            token_type: The type of token to retrieve
            
        Returns:
            List[Token]: A list of tokens for the user with the given type
        """
        pass
    
    @abstractmethod
    def save(self, token: Token) -> Token:
        """
        Save a token.
        
        Args:
            token: The token to save
            
        Returns:
            Token: The saved token
        """
        pass
    
    @abstractmethod
    def delete(self, token_id) -> bool:
        """
        Delete a token.
        
        Args:
            token_id: The ID of the token to delete
            
        Returns:
            bool: True if the token was deleted, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_by_value(self, token_value) -> bool:
        """
        Delete a token by value.
        
        Args:
            token_value: The value of the token to delete
            
        Returns:
            bool: True if the token was deleted, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_by_user_and_type(self, user_id, token_type) -> bool:
        """
        Delete all tokens for a user with a given type.
        
        Args:
            user_id: The ID of the user
            token_type: The type of token to delete
            
        Returns:
            bool: True if the tokens were deleted, False otherwise
        """
        pass


class InvitationRepositoryInterface(ABC):
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


class NotificationRepositoryInterface(ABC):
    """
    Notification repository interface.
    
    This interface defines the methods that a notification repository must implement.
    """
    
    @abstractmethod
    def get_by_id(self, notification_id) -> Optional[Notification]:
        """
        Get a notification by ID.
        
        Args:
            notification_id: The ID of the notification to retrieve
            
        Returns:
            Notification: The notification with the given ID or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id, read=None, limit=None, offset=None) -> List[Notification]:
        """
        Get all notifications for a user.
        
        Args:
            user_id: The ID of the user
            read: Filter by read status (True, False, or None for all)
            limit: Maximum number of notifications to return
            offset: Number of notifications to skip
            
        Returns:
            List[Notification]: A list of notifications for the user
        """
        pass
    
    @abstractmethod
    def create(self, user_id, title, message, type=NotificationType.INFO, link=None) -> Notification:
        """
        Create a notification.
        
        Args:
            user_id: The ID of the user
            title: The notification title
            message: The notification message
            type: The notification type
            link: Optional URL link
            
        Returns:
            Notification: The created notification
        """
        pass
    
    @abstractmethod
    def mark_as_read(self, notification_id) -> Notification:
        """
        Mark a notification as read.
        
        Args:
            notification_id: The ID of the notification
            
        Returns:
            Notification: The updated notification
        """
        pass
    
    @abstractmethod
    def mark_all_as_read(self, user_id) -> int:
        """
        Mark all notifications for a user as read.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            int: The number of notifications marked as read
        """
        pass
    
    @abstractmethod
    def delete(self, notification_id) -> bool:
        """
        Delete a notification.
        
        Args:
            notification_id: The ID of the notification to delete
            
        Returns:
            bool: True if the notification was deleted, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_all_for_user(self, user_id, read=None) -> int:
        """
        Delete all notifications for a user.
        
        Args:
            user_id: The ID of the user
            read: Filter by read status (True, False, or None for all)
            
        Returns:
            int: The number of notifications deleted
        """
        pass

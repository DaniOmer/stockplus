"""
User application interfaces.
This module contains the interfaces for the user application.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class UserRepositoryInterface(ABC):
    """
    User repository interface.
    
    This interface defines the methods that a user repository must implement.
    """
    
    @abstractmethod
    def get_by_id(self, user_id):
        """
        Get a user by ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            User: The user with the given ID or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_email(self, email):
        """
        Get a user by email.
        
        Args:
            email: The email of the user to retrieve
            
        Returns:
            User: The user with the given email or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_phone_number(self, phone_number):
        """
        Get a user by phone number.
        
        Args:
            phone_number: The phone number of the user to retrieve
            
        Returns:
            User: The user with the given phone number or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_username(self, username):
        """
        Get a user by username.
        
        Args:
            username: The username of the user to retrieve
            
        Returns:
            User: The user with the given username or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_company_id(self, company_id):
        """
        Get all users for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            List[User]: A list of users for the company
        """
        pass
    
    @abstractmethod
    def save(self, user):
        """
        Save a user.
        
        Args:
            user: The user to save
            
        Returns:
            User: The saved user
        """
        pass
    
    @abstractmethod
    def update_password(self, user_id, new_password):
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
    def verify_password(self, user_id, password):
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
    def delete(self, user_id):
        """
        Delete a user.
        
        Args:
            user_id: The ID of the user to delete
            
        Returns:
            bool: True if the user was deleted, False otherwise
        """
        pass


class TokenRepositoryInterface(ABC):
    """
    Token repository interface.
    
    This interface defines the methods that a token repository must implement.
    """
    
    @abstractmethod
    def store_verification_token(self, user_id, token, expiry, method='email'):
        """
        Store a verification token.
        
        Args:
            user_id: The ID of the user
            token: The verification token
            expiry: The expiry datetime
            method: The verification method (email or sms)
            
        Returns:
            bool: True if the token was stored successfully
        """
        pass
    
    @abstractmethod
    def get_verification_token(self, token):
        """
        Get a verification token.
        
        Args:
            token: The verification token
            
        Returns:
            dict: The token data or None if not found
        """
        pass
    
    @abstractmethod
    def delete_verification_token(self, token):
        """
        Delete a verification token.
        
        Args:
            token: The verification token
            
        Returns:
            bool: True if the token was deleted
        """
        pass
    
    @abstractmethod
    def store_password_reset_token(self, user_id, token, expiry, method='email'):
        """
        Store a password reset token.
        
        Args:
            user_id: The ID of the user
            token: The password reset token
            expiry: The expiry datetime
            method: The reset method (email or sms)
            
        Returns:
            bool: True if the token was stored successfully
        """
        pass
    
    @abstractmethod
    def get_password_reset_token(self, token):
        """
        Get a password reset token.
        
        Args:
            token: The password reset token
            
        Returns:
            dict: The token data or None if not found
        """
        pass
    
    @abstractmethod
    def delete_password_reset_token(self, token):
        """
        Delete a password reset token.
        
        Args:
            token: The password reset token
            
        Returns:
            bool: True if the token was deleted
        """
        pass


class InvitationRepositoryInterface(ABC):
    """
    Invitation repository interface.
    
    This interface defines the methods that an invitation repository must implement.
    """
    
    @abstractmethod
    def get_by_id(self, invitation_id):
        """
        Get an invitation by ID.
        
        Args:
            invitation_id: The ID of the invitation to retrieve
            
        Returns:
            Invitation: The invitation with the given ID or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_token(self, token):
        """
        Get an invitation by token.
        
        Args:
            token: The token of the invitation to retrieve
            
        Returns:
            Invitation: The invitation with the given token or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_email(self, email):
        """
        Get an invitation by email.
        
        Args:
            email: The email of the invitation to retrieve
            
        Returns:
            Invitation: The invitation with the given email or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_company_id(self, company_id):
        """
        Get all invitations for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            List[Invitation]: A list of invitations for the company
        """
        pass
    
    @abstractmethod
    def save(self, invitation):
        """
        Save an invitation.
        
        Args:
            invitation: The invitation to save
            
        Returns:
            Invitation: The saved invitation
        """
        pass
    
    @abstractmethod
    def delete(self, invitation_id):
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
    def get_by_id(self, notification_id):
        """
        Get a notification by ID.
        
        Args:
            notification_id: The ID of the notification to retrieve
            
        Returns:
            Notification: The notification with the given ID or None if not found
        """
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id):
        """
        Get all notifications for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List[Notification]: A list of notifications for the user
        """
        pass
    
    @abstractmethod
    def save(self, notification):
        """
        Save a notification.
        
        Args:
            notification: The notification to save
            
        Returns:
            Notification: The saved notification
        """
        pass
    
    @abstractmethod
    def mark_as_read(self, notification_id):
        """
        Mark a notification as read.
        
        Args:
            notification_id: The ID of the notification to mark as read
            
        Returns:
            Notification: The updated notification
        """
        pass
    
    @abstractmethod
    def mark_all_as_read(self, user_id):
        """
        Mark all notifications for a user as read.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            int: The number of notifications marked as read
        """
        pass
    
    @abstractmethod
    def delete(self, notification_id):
        """
        Delete a notification.
        
        Args:
            notification_id: The ID of the notification to delete
            
        Returns:
            bool: True if the notification was deleted, False otherwise
        """
        pass

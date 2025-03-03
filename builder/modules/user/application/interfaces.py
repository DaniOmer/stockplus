"""
Application interfaces for the user application.
This module contains the application interfaces for the user application.
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
    def delete(self, user_id):
        """
        Delete a user.

        Args:
            user_id: The ID of the user to delete

        Returns:
            bool: True if the user was deleted, False otherwise
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
    def update_password(self, user_id, new_password):
        """
        Update a user's password.

        Args:
            user_id: The ID of the user
            new_password: The new password

        Returns:
            User: The updated user
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
    def get_by_sender_id(self, sender_id):
        """
        Get all invitations sent by a user.

        Args:
            sender_id: The ID of the sender

        Returns:
            List[Invitation]: A list of invitations sent by the user
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
    def get_by_user_id(self, user_id, read=None, limit=None, offset=None):
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
    def create(self, user_id, title, message, type='INFO', link=None):
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
    def mark_as_read(self, notification_id):
        """
        Mark a notification as read.

        Args:
            notification_id: The ID of the notification

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

    @abstractmethod
    def delete_all_for_user(self, user_id, read=None):
        """
        Delete all notifications for a user.

        Args:
            user_id: The ID of the user
            read: Filter by read status (True, False, or None for all)

        Returns:
            int: The number of notifications deleted
        """
        pass


class TokenRepositoryInterface(ABC):
    """
    Token repository interface.

    This interface defines the methods that a token repository must implement.
    """

    @abstractmethod
    def create_token(self, user_id, token_type, expires_in=None):
        """
        Create a token for a user.

        Args:
            user_id: The ID of the user
            token_type: The type of token to create
            expires_in: The number of seconds until the token expires

        Returns:
            str: The created token
        """
        pass

    @abstractmethod
    def validate_token(self, token, token_type):
        """
        Validate a token.

        Args:
            token: The token to validate
            token_type: The expected token type

        Returns:
            dict: The token payload if valid, None otherwise
        """
        pass

    @abstractmethod
    def invalidate_token(self, token):
        """
        Invalidate a token.

        Args:
            token: The token to invalidate

        Returns:
            bool: True if the token was invalidated, False otherwise
        """
        pass

    @abstractmethod
    def get_user_id_from_token(self, token):
        """
        Get the user ID from a token.

        Args:
            token: The token to extract the user ID from

        Returns:
            int: The user ID if the token is valid, None otherwise
        """
        pass

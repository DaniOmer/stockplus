"""
Application interfaces for the user application.
This module contains the application interfaces for the user application.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from builder.modules.user.domain.models import User, Invitation


class UserRepositoryInterface(ABC):
    """
    User repository interface.
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
    def get_by_username(self, username) -> Optional[User]:
        """
        Get a user by username.

        Args:
            username: The username of the user to retrieve

        Returns:
            User: The user with the given username or None if not found
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
            bool: Whether the password is correct
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


class InvitationRepositoryInterface(ABC):
    """
    Invitation repository interface.
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


class TokenRepositoryInterface(ABC):
    """
    Token repository interface.
    """

    @abstractmethod
    def store_verification_token(self, user_id, token, expiry, method='email'):
        """
        Store a verification token.

        Args:
            user_id: The ID of the user
            token: The token
            expiry: When the token expires
            method: The verification method (email or sms)
        """
        pass

    @abstractmethod
    def get_verification_token(self, token):
        """
        Get a verification token.

        Args:
            token: The token to retrieve

        Returns:
            dict: The token data or None if not found
        """
        pass

    @abstractmethod
    def delete_verification_token(self, token):
        """
        Delete a verification token.

        Args:
            token: The token to delete
        """
        pass

    @abstractmethod
    def store_password_reset_token(self, user_id, token, expiry, method='email'):
        """
        Store a password reset token.

        Args:
            user_id: The ID of the user
            token: The token
            expiry: When the token expires
            method: The reset method (email or sms)
        """
        pass

    @abstractmethod
    def get_password_reset_token(self, token):
        """
        Get a password reset token.

        Args:
            token: The token to retrieve

        Returns:
            dict: The token data or None if not found
        """
        pass

    @abstractmethod
    def delete_password_reset_token(self, token):
        """
        Delete a password reset token.

        Args:
            token: The token to delete
        """
        pass

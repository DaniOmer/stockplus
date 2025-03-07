"""
Domain models for the user application.
This module contains the domain models for the user application.
"""

import secrets
from datetime import datetime, timedelta


class User:
    """
    User domain model.
    """

    def __init__(self, email=None, phone_number=None, username=None,
                 first_name=None, last_name=None, password_hash=None,
                 is_active=True, is_verified=False, company_id=None, role=None,
                 created_at=None, updated_at=None, id=None):
        """
        Initialize a new User instance.

        Args:
            id: The user's ID
            email: The user's email address
            phone_number: The user's phone number
            username: The user's username
            first_name: The user's first name
            last_name: The user's last name
            password_hash: The user's password hash
            is_active: Whether the user is active
            is_verified: Whether the user is verified
            company_id: The ID of the user's company
            role: The user's role in the company
            created_at: When the user was created
            updated_at: When the user was last updated
        """
        self.id = id
        self.email = email
        self.phone_number = phone_number
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
        self.is_active = is_active
        self.is_verified = is_verified
        self.company_id = company_id
        self.role = role
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.verification_tokens = {}
        self.password_reset_tokens = {}

    def verify(self):
        """
        Mark the user as verified.
        """
        self.is_verified = True
        self.updated_at = datetime.now()

    def update_profile(self, email=None, phone_number=None, first_name=None, last_name=None):
        """
        Update the user's profile.

        Args:
            email: The user's new email address
            phone_number: The user's new phone number
            first_name: The user's new first name
            last_name: The user's new last name
        """
        if email is not None:
            self.email = email
        if phone_number is not None:
            self.phone_number = phone_number
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        self.updated_at = datetime.now()

    def assign_to_company(self, company_id, role):
        """
        Assign the user to a company.

        Args:
            company_id: The ID of the company to assign the user to
            role: The user's role in the company
        """
        self.company_id = company_id
        self.role = role
        self.updated_at = datetime.now()

    def remove_from_company(self):
        """
        Remove the user from their company.
        """
        self.company_id = None
        self.role = None
        self.updated_at = datetime.now()

    def deactivate(self):
        """
        Deactivate the user.
        """
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self):
        """
        Activate the user.
        """
        self.is_active = True
        self.updated_at = datetime.now()

    def generate_verification_token(self, method='email'):
        """
        Generate a verification token for the user.

        Args:
            method: The verification method (email or sms)

        Returns:
            str: The verification token
        """
        token = ''.join(secrets.choice('0123456789') for _ in range(6))
        expiry = datetime.now() + timedelta(hours=24)
        
        self.verification_tokens[token] = {
            'method': method,
            'expiry': expiry
        }
        
        return token

    def verify_token(self, token):
        """
        Verify a token.

        Args:
            token: The token to verify

        Returns:
            bool: Whether the token is valid
        """
        if token not in self.verification_tokens:
            return False
        
        token_data = self.verification_tokens[token]
        if token_data['expiry'] < datetime.now():
            del self.verification_tokens[token]
            return False
        
        # Token is valid, remove it and mark user as verified
        del self.verification_tokens[token]
        self.verify()
        return True

    def generate_password_reset_token(self, method='email'):
        """
        Generate a password reset token for the user.

        Args:
            method: The reset method (email or sms)

        Returns:
            str: The password reset token
        """
        token = ''.join(secrets.choice('0123456789') for _ in range(6))
        expiry = datetime.now() + timedelta(hours=1)
        
        self.password_reset_tokens[token] = {
            'method': method,
            'expiry': expiry
        }
        
        return token

    def verify_password_reset_token(self, token):
        """
        Verify a password reset token.

        Args:
            token: The token to verify

        Returns:
            bool: Whether the token is valid
        """
        if token not in self.password_reset_tokens:
            return False
        
        token_data = self.password_reset_tokens[token]
        if token_data['expiry'] < datetime.now():
            del self.password_reset_tokens[token]
            return False
        
        return True

    def clear_password_reset_token(self, token):
        """
        Clear a password reset token.

        Args:
            token: The token to clear
        """
        if token in self.password_reset_tokens:
            del self.password_reset_tokens[token]

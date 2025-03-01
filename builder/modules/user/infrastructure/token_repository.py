"""
Token repository implementation for the user application.
This module contains the token repository implementation for the user application.
"""

from datetime import datetime
import json

from django.conf import settings

from builder.modules.user.application.interfaces import TokenRepositoryInterface


class DjangoModelTokenRepository(TokenRepositoryInterface):
    """
    Django model token repository implementation.
    
    This implementation uses Django models to store tokens.
    """

    def __init__(self):
        """
        Initialize a new DjangoModelTokenRepository instance.
        """
        from builder.modules.user.models import VerificationToken, PasswordResetToken
        self.verification_token_model = VerificationToken
        self.password_reset_token_model = PasswordResetToken

    def store_verification_token(self, user_id, token, expiry, method='email'):
        """
        Store a verification token.

        Args:
            user_id: The ID of the user
            token: The token
            expiry: When the token expires
            method: The verification method (email or sms)
        """
        # Delete any existing tokens for this user
        self.verification_token_model.objects.filter(user_id=user_id).delete()
        
        # Create a new token
        self.verification_token_model.objects.create(
            user_id=user_id,
            token=token,
            expires_at=expiry,
            method=method
        )

    def get_verification_token(self, token):
        """
        Get a verification token.

        Args:
            token: The token to retrieve

        Returns:
            dict: The token data or None if not found
        """
        try:
            token_obj = self.verification_token_model.objects.get(token=token)
            
            # Check if token has expired
            if token_obj.expires_at < datetime.now():
                self.delete_verification_token(token)
                return None
            
            return {
                'user_id': token_obj.user_id,
                'expiry': token_obj.expires_at.timestamp(),
                'method': token_obj.method
            }
        except self.verification_token_model.DoesNotExist:
            return None

    def delete_verification_token(self, token):
        """
        Delete a verification token.

        Args:
            token: The token to delete
        """
        self.verification_token_model.objects.filter(token=token).delete()

    def store_password_reset_token(self, user_id, token, expiry, method='email'):
        """
        Store a password reset token.

        Args:
            user_id: The ID of the user
            token: The token
            expiry: When the token expires
            method: The reset method (email or sms)
        """
        # Delete any existing tokens for this user
        self.password_reset_token_model.objects.filter(user_id=user_id).delete()
        
        # Create a new token
        self.password_reset_token_model.objects.create(
            user_id=user_id,
            token=token,
            expires_at=expiry,
            method=method
        )

    def get_password_reset_token(self, token):
        """
        Get a password reset token.

        Args:
            token: The token to retrieve

        Returns:
            dict: The token data or None if not found
        """
        try:
            token_obj = self.password_reset_token_model.objects.get(token=token)
            
            # Check if token has expired
            if token_obj.expires_at < datetime.now():
                self.delete_password_reset_token(token)
                return None
            
            return {
                'user_id': token_obj.user_id,
                'expiry': token_obj.expires_at.timestamp(),
                'method': token_obj.method
            }
        except self.password_reset_token_model.DoesNotExist:
            return None

    def delete_password_reset_token(self, token):
        """
        Delete a password reset token.

        Args:
            token: The token to delete
        """
        self.password_reset_token_model.objects.filter(token=token).delete()


def get_token_repository():
    """
    Get the token repository.
    
    Returns:
        TokenRepositoryInterface: The token repository
    """
    return DjangoModelTokenRepository()

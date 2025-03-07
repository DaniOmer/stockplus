"""
Token repository implementation.
This module contains the token repository implementation for user verification and password reset.
"""

import logging
from datetime import datetime, timedelta
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

class TokenRepository:
    """
    Token repository implementation.
    
    This class implements the token repository using Django's cache system.
    """
    
    VERIFICATION_PREFIX = 'verification_token_'
    PASSWORD_RESET_PREFIX = 'password_reset_token_'
    
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
        key = f"{self.VERIFICATION_PREFIX}{token}"
        value = {
            'user_id': user_id,
            'method': method,
            'expiry': expiry.timestamp()
        }
        
        # Set the token in the cache with an expiry time
        timeout = int((expiry - datetime.now()).total_seconds())
        cache.set(key, value, timeout=timeout)
        
        return True
    
    def get_verification_token(self, token):
        """
        Get a verification token.
        
        Args:
            token: The verification token
            
        Returns:
            dict: The token data or None if not found
        """
        key = f"{self.VERIFICATION_PREFIX}{token}"
        token_data = cache.get(key)
        
        if not token_data:
            return None
        
        # Check if the token has expired
        expiry = datetime.fromtimestamp(token_data['expiry'])
        if expiry < datetime.now():
            self.delete_verification_token(token)
            return None
        
        return token_data
    
    def delete_verification_token(self, token):
        """
        Delete a verification token.
        
        Args:
            token: The verification token
            
        Returns:
            bool: True if the token was deleted
        """
        key = f"{self.VERIFICATION_PREFIX}{token}"
        cache.delete(key)
        return True
    
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
        key = f"{self.PASSWORD_RESET_PREFIX}{token}"
        value = {
            'user_id': user_id,
            'method': method,
            'expiry': expiry.timestamp()
        }
        
        # Set the token in the cache with an expiry time
        timeout = int((expiry - datetime.now()).total_seconds())
        cache.set(key, value, timeout=timeout)
        
        return True
    
    def get_password_reset_token(self, token):
        """
        Get a password reset token.
        
        Args:
            token: The password reset token
            
        Returns:
            dict: The token data or None if not found
        """
        key = f"{self.PASSWORD_RESET_PREFIX}{token}"
        token_data = cache.get(key)
        
        if not token_data:
            return None
        
        # Check if the token has expired
        expiry = datetime.fromtimestamp(token_data['expiry'])
        if expiry < datetime.now():
            self.delete_password_reset_token(token)
            return None
        
        return token_data
    
    def delete_password_reset_token(self, token):
        """
        Delete a password reset token.
        
        Args:
            token: The password reset token
            
        Returns:
            bool: True if the token was deleted
        """
        key = f"{self.PASSWORD_RESET_PREFIX}{token}"
        cache.delete(key)
        return True


def get_token_repository():
    """
    Get a token repository instance.
    
    Returns:
        TokenRepository: A token repository instance
    """
    return TokenRepository()

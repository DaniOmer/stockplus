"""
Token service for the user application.
This module contains the token service for the user application.
"""

import logging
from typing import List

from stockplus.modules.user.domain.entities import Token, TokenType, TokenMethod
from stockplus.modules.user.application.interfaces import ITokenRepository
from stockplus.modules.user.domain.exceptions import (
    TokenInvalidException,
    TokenExpiredException,
)

logger = logging.getLogger(__name__)

class TokenService:
    """
    Token service.
    
    This class implements the application logic for tokens. It uses the token repository
    to access and manipulate token data and enforces business rules.
    """
    
    def __init__(self, token_repository: ITokenRepository):
        """
        Initialize a new TokenService instance.
        
        Args:
            token_repository: The token repository to use
        """
        self.token_repository = token_repository
    
    def create_verification_token(self, user_id, method=TokenMethod.EMAIL) -> Token:
        """
        Create a verification token.
        
        Args:
            user_id: The ID of the user
            method: The verification method
            
        Returns:
            Token: The created token
        """
        # Delete any existing verification tokens for the user
        self.token_repository.delete_by_user_and_type(user_id, TokenType.VERIFICATION)
        
        # Create a new verification token
        return self.token_repository.create_verification_token(user_id, method)
    
    def create_password_reset_token(self, user_id) -> Token:
        """
        Create a password reset token.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            Token: The created token
        """
        # Delete any existing password reset tokens for the user
        self.token_repository.delete_by_user_and_type(user_id, TokenType.PASSWORD_RESET)
        
        # Create a new password reset token
        return self.token_repository.create_password_reset_token(user_id)
    
    def create_invitation_token(self, user_id, email) -> Token:
        """
        Create an invitation token.
        
        Args:
            user_id: The ID of the user sending the invitation
            email: The email of the invited user
            
        Returns:
            Token: The created token
        """
        # Create a new invitation token
        return self.token_repository.create_invitation_token(user_id, email)
    
    def verify_token(self, token_value, token_type) -> Token:
        """
        Verify a token.
        
        Args:
            token_value: The value of the token to verify
            token_type: The type of token to verify
            
        Returns:
            Token: The verified token
            
        Raises:
            TokenInvalidException: If the token is invalid
            TokenExpiredException: If the token has expired
        """
        # Get the token
        if token_type == TokenType.VERIFICATION:
            token = self.token_repository.get_verification_token(token_value)
        elif token_type == TokenType.PASSWORD_RESET:
            token = self.token_repository.get_password_reset_token(token_value)
        elif token_type == TokenType.INVITATION:
            token = self.token_repository.get_invitation_token(token_value)
        else:
            token = self.token_repository.get_by_value(token_value)
        
        # Check if the token exists
        if not token:
            raise TokenInvalidException("Invalid token")
        
        # Check if the token is valid
        if token.is_used:
            raise TokenInvalidException("Token has already been used")
        
        # Check if the token has expired
        if token.is_expired():
            raise TokenExpiredException("Token has expired")
        
        return token
    
    def use_token(self, token_value, token_type) -> Token:
        """
        Use a token.
        
        Args:
            token_value: The value of the token to use
            token_type: The type of token to use
            
        Returns:
            Token: The used token
            
        Raises:
            TokenInvalidException: If the token is invalid
            TokenExpiredException: If the token has expired
        """
        # Verify the token
        token = self.verify_token(token_value, token_type)
        
        # Mark the token as used
        token.use()
        
        # Save the token
        return self.token_repository.save(token)
    
    def get_tokens_by_user(self, user_id, token_type=None) -> List[Token]:
        """
        Get all tokens for a user.
        
        Args:
            user_id: The ID of the user
            token_type: The type of token to retrieve (optional)
            
        Returns:
            List[Token]: A list of tokens for the user
        """
        if token_type:
            return self.token_repository.get_by_user_and_type(user_id, token_type)
        
        # Get all token types
        verification_tokens = self.token_repository.get_by_user_and_type(user_id, TokenType.VERIFICATION)
        password_reset_tokens = self.token_repository.get_by_user_and_type(user_id, TokenType.PASSWORD_RESET)
        invitation_tokens = self.token_repository.get_by_user_and_type(user_id, TokenType.INVITATION)
        
        # Combine all tokens
        return verification_tokens + password_reset_tokens + invitation_tokens
    
    def delete_expired_tokens(self) -> int:
        """
        Delete all expired tokens.
        
        Returns:
            int: The number of tokens deleted
        """
        # This would be implemented in a real application
        # For now, we'll just return 0
        return 0

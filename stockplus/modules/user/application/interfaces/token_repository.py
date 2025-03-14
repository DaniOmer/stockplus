"""
Application interfaces for the user application.
This module contains the application interfaces for the user application.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from stockplus.modules.user.domain.entities import Token

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
"""
Database token repository implementation.
This module contains the database token repository implementation for the user application.
"""

import logging
from django.db import transaction

from stockplus.modules.user.application.interfaces import ITokenRepository
from stockplus.modules.user.domain.entities import Token, TokenType, TokenMethod
from stockplus.modules.user.infrastructure.models.token_model import Token as TokenModel
from stockplus.modules.user.infrastructure.models.user_model import User as UserModel

logger = logging.getLogger(__name__)

class TokenRepository(ITokenRepository):
    """
    Database token repository implementation.
    
    This class implements the token repository using the database.
    """
    
    def get_by_value(self, token_value):
        """
        Get a token by value.
        
        Args:
            token_value: The value of the token to retrieve
            
        Returns:
            Token: The token with the given value or None if not found
        """
        try:
            token_model = TokenModel.objects.get(token_value=token_value)
            return Token.from_model(token_model)
        except TokenModel.DoesNotExist:
            return None
    
    def get_by_email(self, email):
        """
        Get a token by email.
        
        Args:
            email: The email of the token to retrieve
            
        Returns:
            Token: The token with the given email or None if not found
        """
        try:
            token_model = TokenModel.objects.get(email=email)
            return Token.from_model(token_model)
        except TokenModel.DoesNotExist:
            return None
    
    def get_by_user_and_type(self, user_id, token_type):
        """
        Get all tokens for a user with a given type.
        
        Args:
            user_id: The ID of the user
            token_type: The type of token to retrieve
            
        Returns:
            List[Token]: A list of tokens for the user with the given type
        """
        token_models = TokenModel.objects.filter(
            user_id=user_id,
            token_type=token_type.value if isinstance(token_type, TokenType) else token_type
        )
        return [Token.from_model(token_model) for token_model in token_models]
    
    def save(self, token):
        """
        Save a token.
        
        Args:
            token: The token to save
            
        Returns:
            Token: The saved token
        """
        with transaction.atomic():
            # Get the user model
            user_model = None
            if token.user_id:
                try:
                    user_model = UserModel.objects.get(id=token.user_id)
                except UserModel.DoesNotExist:
                    logger.warning(f"User with ID {token.user_id} not found when saving token")
            
            # Create or update the token model
            if token.id:
                try:
                    token_model = TokenModel.objects.get(id=token.id)
                    token_model.token_value = token.token_value
                    token_model.user = user_model
                    token_model.token_type = token.token_type.value if isinstance(token.token_type, TokenType) else token.token_type
                    token_model.method = token.method.value if isinstance(token.method, TokenMethod) else token.method
                    token_model.expiry = token.expiry
                    token_model.is_used = token.is_used
                    token_model.email = token.email
                    # No need to set date_update as it's auto-updated by Django's auto_now
                    token_model.save()
                except TokenModel.DoesNotExist:
                    logger.warning(f"Token with ID {token.id} not found when updating")
                    return None
            else:
                token_model = TokenModel.objects.create(
                    token_value=token.token_value,
                    user=user_model,
                    token_type=token.token_type.value if isinstance(token.token_type, TokenType) else token.token_type,
                    method=token.method.value if isinstance(token.method, TokenMethod) else token.method,
                    expiry=token.expiry,
                    is_used=token.is_used,
                    email=token.email
                )
            
            # Return the domain entity
            return Token.from_model(token_model)
    
    def delete(self, token_id):
        """
        Delete a token.
        
        Args:
            token_id: The ID of the token to delete
            
        Returns:
            bool: True if the token was deleted, False otherwise
        """
        try:
            token_model = TokenModel.objects.get(id=token_id)
            token_model.delete()
            return True
        except TokenModel.DoesNotExist:
            logger.warning(f"Token with ID {token_id} not found when deleting")
            return False
    
    def delete_by_value(self, token_value):
        """
        Delete a token by value.
        
        Args:
            token_value: The value of the token to delete
            
        Returns:
            bool: True if the token was deleted, False otherwise
        """
        try:
            token_model = TokenModel.objects.get(token_value=token_value)
            token_model.delete()
            return True
        except TokenModel.DoesNotExist:
            logger.warning(f"Token with value {token_value} not found when deleting")
            return False
    
    def delete_by_user_and_type(self, user_id, token_type):
        """
        Delete all tokens for a user with a given type.
        
        Args:
            user_id: The ID of the user
            token_type: The type of token to delete
            
        Returns:
            bool: True if the tokens were deleted, False otherwise
        """
        token_models = TokenModel.objects.filter(
            user_id=user_id,
            token_type=token_type.value if isinstance(token_type, TokenType) else token_type
        )
        token_models.delete()
        return True
    
    def create_verification_token(self, user_id, method=TokenMethod.EMAIL):
        """
        Create a verification token.
        
        Args:
            user_id: The ID of the user
            method: The verification method
            
        Returns:
            Token: The created token
        """
        token = Token(
            user_id=user_id,
            token_type=TokenType.VERIFICATION,
            method=method
        )
        return self.save(token)
    
    def create_password_reset_token(self, user_id):
        """
        Create a password reset token.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            Token: The created token
        """
        token = Token(
            user_id=user_id,
            token_type=TokenType.PASSWORD_RESET,
            method=TokenMethod.EMAIL
        )
        return self.save(token)
    
    def create_invitation_token(self, user_id, email):
        """
        Create an invitation token.
        
        Args:
            user_id: The ID of the user sending the invitation
            email: The email of the invited user
            
        Returns:
            Token: The created token
        """
        token = Token(
            user_id=user_id,
            token_type=TokenType.INVITATION,
            method=TokenMethod.EMAIL,
            email=email
        )
        return self.save(token)
    
    def get_verification_token(self, token_value):
        """
        Get a verification token.
        
        Args:
            token_value: The value of the token to retrieve
            
        Returns:
            Token: The token with the given value or None if not found
        """
        token = self.get_by_value(token_value)
        if token and token.token_type == TokenType.VERIFICATION:
            return token
        return None
    
    def get_password_reset_token(self, token_value):
        """
        Get a password reset token.
        
        Args:
            token_value: The value of the token to retrieve
            
        Returns:
            Token: The token with the given value or None if not found
        """
        token = self.get_by_value(token_value)
        if token and token.token_type == TokenType.PASSWORD_RESET:
            return token
        return None
    
    def get_invitation_token(self, token_value):
        """
        Get an invitation token.
        
        Args:
            token_value: The value of the token to retrieve
            
        Returns:
            Token: The token with the given value or None if not found
        """
        token = self.get_by_value(token_value)
        if token and token.token_type == TokenType.INVITATION:
            return token
        return None

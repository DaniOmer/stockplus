"""
Token domain entity.
This module contains the token domain entity for the user application.
"""
import uuid
from enum import Enum
from datetime import datetime, timedelta, timezone


class TokenType(Enum):
    """
    Token type enum.
    """
    VERIFICATION = 'verification'
    PASSWORD_RESET = 'password_reset'
    INVITATION = 'invitation'


class TokenMethod(Enum):
    """
    Token method enum.
    """
    EMAIL = 'email'
    SMS = 'sms'


class Token:
    """
    Token domain entity.
    
    This class represents a token used for various purposes such as
    email verification, password reset, and invitation.
    """
    
    def __init__(self, id=None, token_value=None, user_id=None, token_type=TokenType.VERIFICATION, 
                 expiry=None, method=TokenMethod.EMAIL, is_used=False, email=None, 
                 created_at=None, updated_at=None):
        """
        Initialize a new Token instance.
        
        Args:
            id: The ID of the token
            token_value: The token value (if None, a new token will be generated)
            user_id: The ID of the user associated with the token
            token_type: The type of token (verification, password_reset, invitation)
            expiry: The expiry datetime (if None, default expiry will be used)
            method: The delivery method (email or sms)
            is_used: Whether the token has been used
            email: The email address (for invitation tokens)
            created_at: When the token was created
            updated_at: When the token was last updated
        """
        self.id = id
        self.token_value = token_value or self._generate_token(token_type)
        self.user_id = user_id
        self.token_type = token_type
        self.expiry = expiry or self._get_default_expiry(token_type)
        self.method = method
        self.is_used = is_used
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at
        
    def _generate_token(self, token_type):
        """
        Generate a secure random token.
        
        Args:
            token_type: The type of token to generate
            
        Returns:
            str: The generated token
        """
        token_length = 6 if token_type == TokenType.VERIFICATION else 15
        return uuid.uuid4().hex[:token_length]
    
    def _get_default_expiry(self, token_type):
        """
        Get the default expiry time for a token type.
        
        Args:
            token_type: The type of token
            
        Returns:
            datetime: The expiry datetime
        """
        now = datetime.now(timezone.utc)
        if token_type == TokenType.VERIFICATION:
            # 24 hours for verification tokens
            return now + timedelta(minutes=15)
        elif token_type == TokenType.PASSWORD_RESET:
            # 1 hour for password reset tokens
            return now + timedelta(hours=1)
        elif token_type == TokenType.INVITATION:
            # 7 days for invitation tokens
            return now + timedelta(days=7)
        else:
            # Default to 24 hours
            return now + timedelta(hours=24)
    
    def is_expired(self):
        """
        Check if the token has expired.
        
        Returns:
            bool: True if the token has expired, False otherwise
        """
        return datetime.now(timezone.utc) > self.expiry
    
    def is_valid(self):
        """
        Check if the token is valid.
        
        Returns:
            bool: True if the token is valid, False otherwise
        """
        return not self.is_used and not self.is_expired()
    
    def use(self):
        """
        Mark the token as used.
        """
        self.is_used = True
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """
        Convert the token to a dictionary.
        
        Returns:
            dict: The token as a dictionary
        """
        return {
            'id': self.id,
            'token_value': self.token_value,
            'user_id': self.user_id,
            'token_type': self.token_type.value,
            'expiry': self.expiry.timestamp() if self.expiry else None,
            'method': self.method.value if isinstance(self.method, TokenMethod) else self.method,
            'is_used': self.is_used,
            'email': self.email,
            'created_at': self.created_at.timestamp() if self.created_at else None,
            'updated_at': self.updated_at.timestamp() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a token from a dictionary.
        
        Args:
            data: The dictionary containing token data
            
        Returns:
            Token: The created token
        """
        if not data:
            return None
            
        return cls(
            id=data.get('id'),
            token_value=data.get('token_value'),
            user_id=data.get('user_id'),
            token_type=TokenType(data.get('token_type')) if data.get('token_type') else TokenType.VERIFICATION,
            expiry=datetime.fromtimestamp(data.get('expiry')) if data.get('expiry') else None,
            method=TokenMethod(data.get('method')) if data.get('method') else TokenMethod.EMAIL,
            is_used=data.get('is_used', False),
            email=data.get('email'),
            created_at=datetime.fromtimestamp(data.get('created_at')) if data.get('created_at') else None,
            updated_at=datetime.fromtimestamp(data.get('updated_at')) if data.get('updated_at') else None
        )
    
    @classmethod
    def from_model(cls, model):
        """
        Create a token from a model.
        
        Args:
            model: The model to create the token from
            
        Returns:
            Token: The created token
        """
        if not model:
            return None
            
        return cls(
            id=model.id,
            token_value=model.token_value,
            user_id=model.user.id if model.user else None,
            token_type=TokenType(model.token_type),
            expiry=model.expiry,
            method=TokenMethod(model.method),
            is_used=model.is_used,
            email=model.email,
            created_at=model.created_at if hasattr(model, 'created_at') else None,
            updated_at=model.updated_at if hasattr(model, 'updated_at') else None
        )

"""
Application services for the user application.
This module contains the application services for the user application.
"""

import logging
from typing import List, Optional, Dict, Any

from stockplus.modules.user.domain.entities.user import User
from stockplus.modules.user.domain.exceptions import (
    UserNotFoundException,
    InvalidCredentialsException,
    UserAlreadyExistsException,
    ValidationException,
)
from stockplus.modules.user.application.interfaces import IUserRepository
from stockplus.modules.user.application.services import TokenService, TokenType

logger = logging.getLogger(__name__)


class UserService:
    """
    User service.
    
    This class implements the application logic for the user module. It uses the user repository
    to access and manipulate user data and enforces business rules.
    """
    
    def __init__(
        self, 
        user_repository: IUserRepository, 
        token_service: TokenService,
    ):
        """
        Initialize a new UserService instance.
        
        Args:
            user_repository: The user repository to use
            token_service: The token service to use
            jwt_token_service: The JWT token service to use
        """
        self.user_repository = user_repository
        self.token_service = token_service

    def get_all_users(self) -> List[User]:
        """
        Get all users.
        """
        return self.user_repository.get_all()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            User: The user with the given ID or None if not found
        """
        return self.user_repository.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            email: The email of the user to retrieve
            
        Returns:
            User: The user with the given email or None if not found
        """
        return self.user_repository.get_by_email(email)
    
    def get_user_by_phone_number(self, phone_number: str) -> Optional[User]:
        """
        Get a user by phone number.
        
        Args:
            phone_number: The phone number of the user to retrieve
            
        Returns:
            User: The user with the given phone number or None if not found
        """
        return self.user_repository.get_by_phone_number(phone_number)
    
    def get_users_by_company_id(self, company_id: int) -> List[User]:
        """
        Get all users for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            List[User]: A list of users for the company
        """
        return self.user_repository.get_by_company_id(company_id)
    
    def create_user(self, email=None, phone_number=None, password=None, first_name=None, last_name=None, **extra_fields) -> User:
        """
        Create a new user.
        
        Args:
            email: The user's email address
            phone_number: The user's phone number
            password: The user's password
            first_name: The user's first name
            last_name: The user's last name
            **extra_fields: Additional user data
            
        Returns:
            User: The created user
            
        Raises:
            ValidationException: If neither email nor phone_number is provided
            UserAlreadyExistsException: If a user with the given email or phone number already exists
        """
        if not email and not phone_number:
            raise ValidationException("Either email or phone_number must be provided")
        
        # Check if a user with the given email or phone number already exists
        if email and self.user_repository.get_by_email(email):
            raise UserAlreadyExistsException(f"A user with email {email} already exists")
        
        if phone_number and self.user_repository.get_by_phone_number(phone_number):
            raise UserAlreadyExistsException(f"A user with phone number {phone_number} already exists")
        
        # Create a new user entity
        user = User(
            email=email,
            phone_number=phone_number,
            password_hash=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        
        # Save the user
        created_user = self.user_repository.save(user)
        return created_user
    
    def update_user(self, user_id, email=None, phone_number=None, first_name=None, last_name=None, **extra_fields) -> User:
        """
        Update a user.
        
        Args:
            user_id: The ID of the user to update
            email: The user's new email address
            phone_number: The user's new phone number
            first_name: The user's new first name
            last_name: The user's new last name
            **extra_fields: Additional user data
            
        Returns:
            User: The updated user
            
        Raises:
            UserNotFoundException: If the user is not found
            UserAlreadyExistsException: If a user with the given email or phone number already exists
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        
        # Check if a user with the given email already exists
        if email is not None and email != user.email:
            existing_user = self.user_repository.get_by_email(email)
            if existing_user and existing_user.id != user.id:
                raise UserAlreadyExistsException(f"A user with email {email} already exists")
            user.email = email
            
        # Check if a user with the given phone number already exists
        if phone_number is not None and phone_number != user.phone_number:
            existing_user = self.user_repository.get_by_phone_number(phone_number)
            if existing_user and existing_user.id != user.id:
                raise UserAlreadyExistsException(f"A user with phone number {phone_number} already exists")
            user.phone_number = phone_number
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        
        # Update extra fields
        for key, value in extra_fields.items():
            setattr(user, key, value)
        
        # Save the user
        return self.user_repository.save(user)
    
    def verify_user(self, user_id) -> User:
        """
        Verify a user.
        
        Args:
            user_id: The ID of the user to verify
            
        Returns:
            User: The verified user
            
        Raises:
            UserNotFoundException: If the user is not found
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        
        # Verify the user
        user.is_verified = True
        
        # Save the user
        return self.user_repository.save(user)
    
    def update_password(self, user_id, new_password) -> User:
        """
        Update a user's password.
        
        Args:
            user_id: The ID of the user to update
            new_password: The new password
            
        Returns:
            User: The updated user
            
        Raises:
            UserNotFoundException: If the user is not found
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        
        # Update the password
        return self.user_repository.update_password(user_id, new_password)
    
    def verify_password(self, user_id, password) -> bool:
        """
        Verify a user's password.
        
        Args:
            user_id: The ID of the user
            password: The password to verify
            
        Returns:
            bool: True if the password is correct, False otherwise
            
        Raises:
            UserNotFoundException: If the user is not found
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        
        # Verify the password
        return self.user_repository.verify_password(user_id, password)
    
    def authenticate(self, email=None, phone_number=None, password=None) -> User:
        """
        Authenticate a user.
        
        Args:
            email: The user's email address
            phone_number: The user's phone number
            password: The user's password
            
        Returns:
            User: The authenticated user
            
        Raises:
            InvalidCredentialsException: If the credentials are invalid
        """
        user = None
        
        if email:
            user = self.user_repository.get_by_email(email=email, raw=True)
        elif phone_number:
            user = self.user_repository.get_by_phone_number(phone_number=phone_number, raw=True)
        
        if not user:
            raise InvalidCredentialsException("Invalid credentials")
        
        if not self.user_repository.verify_password(user.id, password):
            raise InvalidCredentialsException("Invalid credentials")
        
        return user
    
    def delete_user(self, user_id) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: The ID of the user to delete
            
        Returns:
            bool: True if the user was deleted, False otherwise
            
        Raises:
            UserNotFoundException: If the user is not found
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        
        # Delete the user
        return self.user_repository.delete(user_id)
    
    def assign_to_company(self, user_id, company_id, role) -> User:
        """
        Assign a user to a company.
        
        Args:
            user_id: The ID of the user to assign
            company_id: The ID of the company to assign the user to
            role: The user's role in the company
            
        Returns:
            User: The updated user
            
        Raises:
            UserNotFoundException: If the user is not found
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        
        # Assign the user to the company
        user.company_id = company_id
        user.role = role
        
        # Save the user
        return self.user_repository.save(user)
    
    def remove_from_company(self, user_id) -> User:
        """
        Remove a user from their company.
        
        Args:
            user_id: The ID of the user to remove
            
        Returns:
            User: The updated user
            
        Raises:
            UserNotFoundException: If the user is not found
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        
        # Remove the user from their company
        user.company_id = None
        user.role = None
        
        # Save the user
        return self.user_repository.save(user)
    
    def generate_verification_token(self, user_id, method='email') -> str:
        """
        Generate a verification token for a user.
        
        Args:
            user_id: The ID of the user
            method: The verification method (email or sms)
            
        Returns:
            str: The verification token
        """
        # Use the token service to generate and store a token
        return self.token_service.create_verification_token(user_id, method)
    
    def validate_verification_token(self, token_value) -> Dict[str, Any]:
        """
        Verify a token.
        
        Args:
            token_value: The token value to verify
            
        Returns:
            Dict[str, Any]: The token data
            
        Raises:
            TokenInvalidException: If the token is invalid
            TokenExpiredException: If the token has expired
        """
        # Get the token
        token = self.token_service.use_token(token_value, TokenType.VERIFICATION)
        
        # Convert token to dict for backward compatibility
        return {
            'user_id': token.user_id,
            'method': token.method,
            'type': token.token_type.value
        }
    
    def generate_password_reset_token(self, email=None, phone_number=None) -> str:
        """
        Generate a password reset token for a user.
        
        Args:
            email: The user's email address
            phone_number: The user's phone number (not used, password reset is email only)
            
        Returns:
            str: The password reset token
            
        Raises:
            UserNotFoundException: If the user is not found
        """
        # Password reset is only via email
        if not email:
            raise ValidationException("Email is required for password reset")
        
        user = self.user_repository.get_by_email(email)
        
        if not user:
            raise UserNotFoundException("User not found")
        
        # Use the token repository to create a token
        return self.token_service.create_password_reset_token(user.id)
    
    def verify_password_reset_token(self, token_value) -> Dict[str, Any]:
        """
        Verify a password reset token.
        
        Args:
            token_value: The token value to verify
            
        Returns:
            Dict[str, Any]: The token data
            
        Raises:
            TokenInvalidException: If the token is invalid
            TokenExpiredException: If the token has expired
        """
        # Get the token
        token = self.token_service.use_token(token_value, TokenType.PASSWORD_RESET)
        
        # Convert token to dict for backward compatibility
        return {
            'id': token.id,
            'user_id': token.user_id,
            'method': token.method,
            'type': token.token_type.value
        }
    
    def reset_password(self, token_value, new_password) -> User:
        """
        Reset a user's password.
        
        Args:
            token_value: The password reset token value
            new_password: The new password
            
        Returns:
            User: The updated user
            
        Raises:
            TokenInvalidException: If the token is invalid
            TokenExpiredException: If the token has expired
            UserNotFoundException: If the user is not found
        """
        # Verify the token
        token_data = self.verify_password_reset_token(token_value)
        
        # Get the user
        user_id = token_data['user_id']
        user = self.user_repository.get_by_id(user_id)
        
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        
        # Update the password
        user = self.user_repository.update_password(user_id, new_password)
        
        return user
    
    def login(self, email=None, phone_number=None, password=None) -> dict:
        """
        Login a user and generate JWT tokens.
        
        Args:
            email: The user's email address
            phone_number: The user's phone number
            password: The user's password
            
        Returns:
            dict: A dictionary containing the access and refresh tokens
            
        Raises:
            InvalidCredentialsException: If the credentials are invalid
        """
        # Authenticate the user
        user = self.authenticate(email=email, phone_number=phone_number, password=password)
        return user

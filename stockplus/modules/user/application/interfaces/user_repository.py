"""
Application interfaces for the user application.
This module contains the application interfaces for the user application.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from stockplus.modules.user.domain.entities import User

class IUserRepository(ABC):
    """
    User repository interface.
    
    This interface defines the methods that a user repository must implement.
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
            bool: True if the password is correct, False otherwise
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
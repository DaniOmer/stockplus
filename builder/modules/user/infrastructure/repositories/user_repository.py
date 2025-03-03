"""
User repository implementation.
This module contains the user repository implementation.
"""

from typing import List, Optional
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password

from builder.models import User as UserORM
from builder.modules.user.application.interfaces import (
    UserRepositoryInterface,
)

User = get_user_model()

class UserRepository(UserRepositoryInterface):
    """
    User repository implementation.

    This class implements the UserRepositoryInterface using Django ORM.
    """

    def get_by_id(self, user_id) -> Optional[UserORM]:
        """
        Get a user by ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            User: The user with the given ID or None if not found
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get_by_email(self, email) -> Optional[UserORM]:
        """
        Get a user by email.

        Args:
            email: The email of the user to retrieve

        Returns:
            User: The user with the given email or None if not found
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_by_phone_number(self, phone_number) -> Optional[UserORM]:
        """
        Get a user by phone number.

        Args:
            phone_number: The phone number of the user to retrieve

        Returns:
            User: The user with the given phone number or None if not found
        """
        try:
            return User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None

    def get_by_username(self, username) -> Optional[UserORM]:
        """
        Get a user by username.

        Args:
            username: The username of the user to retrieve

        Returns:
            User: The user with the given username or None if not found
        """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get_by_company_id(self, company_id) -> List[UserORM]:
        """
        Get all users for a company.

        Args:
            company_id: The ID of the company

        Returns:
            List[User]: A list of users for the company
        """
        return list(User.objects.filter(company_id=company_id))

    def save(self, user: UserORM) -> UserORM:
        """
        Save a user.

        Args:
            user: The user to save

        Returns:
            User: The saved user
        """
        # If the user is new and has a password_hash attribute, hash the password
        if not user.id and hasattr(user, 'password_hash') and user.password_hash:
            user.password = make_password(user.password_hash)
            delattr(user, 'password_hash')

        user.save()
        return user

    def update_password(self, user_id, new_password) -> UserORM:
        """
        Update a user's password.

        Args:
            user_id: The ID of the user to update
            new_password: The new password

        Returns:
            User: The updated user
        """
        user = self.get_by_id(user_id)
        if user:
            user.password = make_password(new_password)
            user.save()
        return user

    def verify_password(self, user_id, password) -> bool:
        """
        Verify a user's password.

        Args:
            user_id: The ID of the user
            password: The password to verify

        Returns:
            bool: True if the password is correct, False otherwise
        """
        user = self.get_by_id(user_id)
        if not user:
            return False
        return check_password(password, user.password)

    def delete(self, user_id) -> bool:
        """
        Delete a user.

        Args:
            user_id: The ID of the user to delete

        Returns:
            bool: True if the user was deleted, False otherwise
        """
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False
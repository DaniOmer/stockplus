"""
User repository implementation.
This module contains the user repository implementation.
"""

from typing import List, Optional
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password

from stockplus.modules.user.domain.entities import User
from stockplus.modules.user.application.interfaces import (
    UserRepositoryInterface,
)

UserORM = get_user_model()

class UserRepository(UserRepositoryInterface):
    """
    User repository implementation.

    This class implements the UserRepositoryInterface using Django ORM.
    """

    def _to_domain_entity(self, user_orm) -> User:
        """
        Convert a User ORM model to a User domain entity.

        Args:
            user_orm: The User ORM model to convert

        Returns:
            User: The User domain entity
        """
        if not user_orm:
            return None
        
        return User(
            id=user_orm.id,
            email=user_orm.email,
            phone_number=user_orm.phone_number,
            username=user_orm.username,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            is_active=user_orm.is_active,
            is_verified=user_orm.is_verified,
            company_id=user_orm.company_id,
            role=user_orm.role,
            created_at=user_orm.date_joined,
            updated_at=user_orm.date_joined
        )

    def get_by_id(self, user_id) -> Optional[User]:
        """
        Get a user by ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            User: The user with the given ID or None if not found
        """
        try:
            user_orm = UserORM.objects.get(id=user_id)
            return self._to_domain_entity(user_orm)
        except UserORM.DoesNotExist:
            return None

    def get_by_email(self, email) -> Optional[User]:
        """
        Get a user by email.

        Args:
            email: The email of the user to retrieve

        Returns:
            User: The user with the given email or None if not found
        """
        try:
            user_orm = UserORM.objects.get(email=email)
            return self._to_domain_entity(user_orm)
        except UserORM.DoesNotExist:
            return None

    def get_by_phone_number(self, phone_number) -> Optional[User]:
        """
        Get a user by phone number.

        Args:
            phone_number: The phone number of the user to retrieve

        Returns:
            User: The user with the given phone number or None if not found
        """
        try:
            user_orm = UserORM.objects.get(phone_number=phone_number)
            return self._to_domain_entity(user_orm)
        except UserORM.DoesNotExist:
            return None

    def get_by_username(self, username) -> Optional[User]:
        """
        Get a user by username.

        Args:
            username: The username of the user to retrieve

        Returns:
            User: The user with the given username or None if not found
        """
        try:
            user_orm = UserORM.objects.get(username=username)
            return self._to_domain_entity(user_orm)
        except UserORM.DoesNotExist:
            return None

    def get_by_company_id(self, company_id) -> List[User]:
        """
        Get all users for a company.

        Args:
            company_id: The ID of the company

        Returns:
            List[User]: A list of users for the company
        """
        user_orms = UserORM.objects.filter(company_id=company_id)
        return [self._to_domain_entity(user_orm) for user_orm in user_orms]

    def save(self, user: User) -> User:
        """
        Save a user, either creating a new one or updating an existing one.

        Args:
            user: The user to save.

        Returns:
            User: The saved user.
        """
        COMMON_FIELDS = [
            'email', 'phone_number', 'username', 'first_name',
            'last_name', 'is_active', 'is_verified', 'company_id', 'role'
        ]

        # Check for existing user using filter().first() for cleaner existence check
        existing_user = UserORM.objects.filter(id=user.id).first() if user.id else None

        # Handle password hashing once for both create/update scenarios
        hashed_password = None
        if hasattr(user, 'password_hash') and user.password_hash:
            hashed_password = make_password(user.password_hash)

        if not existing_user:
            # Create new user with dictionary unpacking
            user_data = {field: getattr(user, field) for field in COMMON_FIELDS}
            user_data['password'] = hashed_password
            return UserORM.objects.create(**user_data)
        else:
            # Update existing user using dynamic field assignment
            for field in COMMON_FIELDS:
                setattr(existing_user, field, getattr(user, field))
            
            # Only update password if new hash was provided
            if hashed_password is not None:
                existing_user.password = hashed_password
            
            existing_user.save()
            return existing_user

    def update_password(self, user_id, new_password) -> User:
        """
        Update a user's password.

        Args:
            user_id: The ID of the user to update
            new_password: The new password

        Returns:
            User: The updated user
        """
        try:
            user_orm = UserORM.objects.get(id=user_id)
            user_orm.password = make_password(new_password)
            user_orm.save()
            return self._to_domain_entity(user_orm)
        except UserORM.DoesNotExist:
            return None

    def verify_password(self, user_id, password) -> bool:
        """
        Verify a user's password.

        Args:
            user_id: The ID of the user
            password: The password to verify

        Returns:
            bool: True if the password is correct, False otherwise
        """
        try:
            user_orm = UserORM.objects.get(id=user_id)
            return check_password(password, user_orm.password)
        except UserORM.DoesNotExist:
            return False

    def delete(self, user_id) -> bool:
        """
        Delete a user.

        Args:
            user_id: The ID of the user to delete

        Returns:
            bool: True if the user was deleted, False otherwise
        """
        try:
            user_orm = UserORM.objects.get(id=user_id)
            user_orm.delete()
            return True
        except UserORM.DoesNotExist:
            return False

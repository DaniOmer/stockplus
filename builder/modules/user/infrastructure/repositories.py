"""
Infrastructure repositories for the user application.
This module contains the infrastructure repositories for the user application.
"""

from typing import List, Optional
import uuid
from datetime import datetime
import hashlib
import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction

from builder.modules.user.domain.models import User, Invitation
from builder.modules.user.application.interfaces import (
    UserRepositoryInterface,
    InvitationRepositoryInterface
)
from builder.modules.user.models import Invitation as InvitationModel


class UserRepository(UserRepositoryInterface):
    """
    User repository implementation.
    """

    def __init__(self):
        """
        Initialize a new UserRepository instance.
        """
        self.user_model = get_user_model()

    def get_by_id(self, user_id) -> Optional[User]:
        """
        Get a user by ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            User: The user with the given ID or None if not found
        """
        try:
            user_orm = self.user_model.objects.get(id=user_id)
            return self._to_domain(user_orm)
        except self.user_model.DoesNotExist:
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
            user_orm = self.user_model.objects.get(email=email)
            return self._to_domain(user_orm)
        except self.user_model.DoesNotExist:
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
            user_orm = self.user_model.objects.get(phone_number=phone_number)
            return self._to_domain(user_orm)
        except self.user_model.DoesNotExist:
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
            user_orm = self.user_model.objects.get(username=username)
            return self._to_domain(user_orm)
        except self.user_model.DoesNotExist:
            return None

    def get_by_company_id(self, company_id) -> List[User]:
        """
        Get all users for a company.

        Args:
            company_id: The ID of the company

        Returns:
            List[User]: A list of users for the company
        """
        user_orms = self.user_model.objects.filter(company_id=company_id)
        return [self._to_domain(user_orm) for user_orm in user_orms]

    def save(self, user: User) -> User:
        """
        Save a user.

        Args:
            user: The user to save

        Returns:
            User: The saved user
        """
        if user.id is None:
            # Create new user
            user_orm = self.user_model(
                email=user.email,
                phone_number=user.phone_number,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                is_verified=user.is_verified,
                company_id=user.company_id,
                role=user.role
            )
            
            # Set password if provided
            if user.password_hash:
                user_orm.set_password(user.password_hash)
            
            user_orm.save()
            
            # Update domain model with generated ID
            user.id = user_orm.id
        else:
            # Update existing user
            try:
                user_orm = self.user_model.objects.get(id=user.id)
                
                user_orm.email = user.email
                user_orm.phone_number = user.phone_number
                user_orm.username = user.username
                user_orm.first_name = user.first_name
                user_orm.last_name = user.last_name
                user_orm.is_active = user.is_active
                user_orm.is_verified = user.is_verified
                user_orm.company_id = user.company_id
                user_orm.role = user.role
                
                user_orm.save()
            except self.user_model.DoesNotExist:
                return None
        
        # Store verification tokens and password reset tokens in cache or database
        # In a real implementation, you would store these in Redis or a similar cache
        # For now, we'll just keep them in memory on the domain model
        
        return user

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
            user_orm = self.user_model.objects.get(id=user_id)
            user_orm.set_password(new_password)
            user_orm.save()
            
            return self._to_domain(user_orm)
        except self.user_model.DoesNotExist:
            return None

    def verify_password(self, user_id, password) -> bool:
        """
        Verify a user's password.

        Args:
            user_id: The ID of the user
            password: The password to verify

        Returns:
            bool: Whether the password is correct
        """
        try:
            user_orm = self.user_model.objects.get(id=user_id)
            return user_orm.check_password(password)
        except self.user_model.DoesNotExist:
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
            user_orm = self.user_model.objects.get(id=user_id)
            user_orm.delete()
            return True
        except self.user_model.DoesNotExist:
            return False

    def _to_domain(self, user_orm) -> User:
        """
        Convert a user ORM model to a domain model.

        Args:
            user_orm: The user ORM model to convert

        Returns:
            User: The domain model
        """
        return User(
            id=user_orm.id,
            email=user_orm.email,
            phone_number=user_orm.phone_number,
            username=user_orm.username,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            password_hash=None,  # Don't expose password hash
            is_active=user_orm.is_active,
            is_verified=user_orm.is_verified,
            company_id=user_orm.company_id if hasattr(user_orm, 'company_id') else None,
            role=user_orm.role if hasattr(user_orm, 'role') else None,
            created_at=user_orm.date_joined if hasattr(user_orm, 'date_joined') else None,
            updated_at=user_orm.last_login if hasattr(user_orm, 'last_login') else None
        )


class InvitationRepository(InvitationRepositoryInterface):
    """
    Invitation repository implementation.
    """

    def get_by_id(self, invitation_id) -> Optional[Invitation]:
        """
        Get an invitation by ID.

        Args:
            invitation_id: The ID of the invitation to retrieve

        Returns:
            Invitation: The invitation with the given ID or None if not found
        """
        try:
            invitation_orm = InvitationModel.objects.get(id=invitation_id)
            return self._to_domain(invitation_orm)
        except InvitationModel.DoesNotExist:
            return None

    def get_by_email(self, email) -> Optional[Invitation]:
        """
        Get an invitation by email.

        Args:
            email: The email of the invitation to retrieve

        Returns:
            Invitation: The invitation with the given email or None if not found
        """
        try:
            invitation_orm = InvitationModel.objects.get(email=email, status='PENDING')
            return self._to_domain(invitation_orm)
        except InvitationModel.DoesNotExist:
            return None

    def get_by_token(self, token) -> Optional[Invitation]:
        """
        Get an invitation by token.

        Args:
            token: The token of the invitation to retrieve

        Returns:
            Invitation: The invitation with the given token or None if not found
        """
        try:
            invitation_orm = InvitationModel.objects.get(token=token)
            return self._to_domain(invitation_orm)
        except InvitationModel.DoesNotExist:
            return None

    def get_by_sender_id(self, sender_id) -> List[Invitation]:
        """
        Get all invitations sent by a user.

        Args:
            sender_id: The ID of the sender

        Returns:
            List[Invitation]: A list of invitations sent by the user
        """
        invitation_orms = InvitationModel.objects.filter(sender_id=sender_id)
        return [self._to_domain(invitation_orm) for invitation_orm in invitation_orms]

    def save(self, invitation: Invitation) -> Invitation:
        """
        Save an invitation.

        Args:
            invitation: The invitation to save

        Returns:
            Invitation: The saved invitation
        """
        if invitation.id is None:
            # Create new invitation
            invitation_orm = InvitationModel(
                email=invitation.email,
                token=invitation.token,
                sender_id=invitation.sender_id,
                status=invitation.status,
                expires_at=invitation.expires_at
            )
            invitation_orm.save()
            
            # Update domain model with generated ID
            invitation.id = invitation_orm.id
        else:
            # Update existing invitation
            try:
                invitation_orm = InvitationModel.objects.get(id=invitation.id)
                
                invitation_orm.email = invitation.email
                invitation_orm.token = invitation.token
                invitation_orm.sender_id = invitation.sender_id
                invitation_orm.status = invitation.status
                invitation_orm.expires_at = invitation.expires_at
                
                invitation_orm.save()
            except InvitationModel.DoesNotExist:
                return None
        
        return invitation

    def delete(self, invitation_id) -> bool:
        """
        Delete an invitation.

        Args:
            invitation_id: The ID of the invitation to delete

        Returns:
            bool: True if the invitation was deleted, False otherwise
        """
        try:
            invitation_orm = InvitationModel.objects.get(id=invitation_id)
            invitation_orm.delete()
            return True
        except InvitationModel.DoesNotExist:
            return False

    def _to_domain(self, invitation_orm) -> Invitation:
        """
        Convert an invitation ORM model to a domain model.

        Args:
            invitation_orm: The invitation ORM model to convert

        Returns:
            Invitation: The domain model
        """
        return Invitation(
            id=invitation_orm.id,
            email=invitation_orm.email,
            token=invitation_orm.token,
            sender_id=invitation_orm.sender_id,
            status=invitation_orm.status,
            expires_at=invitation_orm.expires_at,
            created_at=invitation_orm.created_at,
            updated_at=invitation_orm.updated_at
        )

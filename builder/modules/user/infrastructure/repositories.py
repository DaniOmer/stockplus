"""
Repository implementations for the user application.
This module contains the repository implementations for the user application.
"""

from typing import List, Optional
from django.db import transaction
from django.contrib.auth import get_user_model

from builder.models import Invitation as InvitationORM
from builder.modules.user.domain.models import User, Invitation
from builder.modules.user.application.interfaces import (
    UserRepositoryInterface,
    InvitationRepositoryInterface
)

DjangoUser = get_user_model()


class UserRepository(UserRepositoryInterface):
    """
    Implementation of the user repository interface using Django ORM.
    """
    
    def get_by_id(self, user_id) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            User: The user with the given ID, or None if not found
        """
        try:
            user_orm = DjangoUser.objects.get(id=user_id)
            return self._to_domain(user_orm)
        except DjangoUser.DoesNotExist:
            return None
    
    def get_by_email(self, email) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            email: The email of the user to retrieve
            
        Returns:
            User: The user with the given email, or None if not found
        """
        try:
            user_orm = DjangoUser.objects.get(email=email)
            return self._to_domain(user_orm)
        except DjangoUser.DoesNotExist:
            return None
    
    def get_by_phone_number(self, phone_number) -> Optional[User]:
        """
        Get a user by phone number.
        
        Args:
            phone_number: The phone number of the user to retrieve
            
        Returns:
            User: The user with the given phone number, or None if not found
        """
        try:
            user_orm = DjangoUser.objects.get(phone_number=phone_number)
            return self._to_domain(user_orm)
        except DjangoUser.DoesNotExist:
            return None
    
    def get_by_username(self, username) -> Optional[User]:
        """
        Get a user by username.
        
        Args:
            username: The username of the user to retrieve
            
        Returns:
            User: The user with the given username, or None if not found
        """
        try:
            user_orm = DjangoUser.objects.get(username=username)
            return self._to_domain(user_orm)
        except DjangoUser.DoesNotExist:
            return None
    
    def get_by_company_id(self, company_id) -> List[User]:
        """
        Get all users for a company.
        
        Args:
            company_id: The ID of the company
            
        Returns:
            List[User]: A list of users for the company
        """
        user_orms = DjangoUser.objects.filter(company_id=company_id)
        return [self._to_domain(user_orm) for user_orm in user_orms]
    
    @transaction.atomic
    def save(self, user: User) -> User:
        """
        Save a user.
        
        This method creates a new user if the user doesn't have an ID,
        or updates an existing user if the user has an ID.
        
        Args:
            user: The user to save
            
        Returns:
            User: The saved user with updated information (e.g., ID if it was a new user)
        """
        if user.id:
            try:
                user_orm = DjangoUser.objects.get(id=user.id)
                # Update existing user
                user_orm.email = user.email
                user_orm.username = user.username
                user_orm.phone_number = user.phone_number
                user_orm.first_name = user.first_name
                user_orm.last_name = user.last_name
                user_orm.date_of_birth = user.date_of_birth
                user_orm.is_active = user.is_active
                user_orm.is_verified = user.is_verified
                user_orm.first_connection = user.first_connection
                
                if hasattr(user_orm, 'company_id'):
                    user_orm.company_id = user.company_id
                
                if hasattr(user_orm, 'role'):
                    user_orm.role = user.role
                
                if user.password_hash:
                    user_orm.set_password(user.password_hash)
                
                user_orm.save()
            except DjangoUser.DoesNotExist:
                # Create new user with existing ID
                user_orm = DjangoUser(
                    id=user.id,
                    email=user.email,
                    username=user.username,
                    phone_number=user.phone_number,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    date_of_birth=user.date_of_birth,
                    is_active=user.is_active,
                    is_verified=user.is_verified,
                    first_connection=user.first_connection
                )
                
                if hasattr(user_orm, 'company_id'):
                    user_orm.company_id = user.company_id
                
                if hasattr(user_orm, 'role'):
                    user_orm.role = user.role
                
                if user.password_hash:
                    user_orm.set_password(user.password_hash)
                
                user_orm.save()
        else:
            # Create new user
            user_orm = DjangoUser(
                email=user.email,
                username=user.username,
                phone_number=user.phone_number,
                first_name=user.first_name,
                last_name=user.last_name,
                date_of_birth=user.date_of_birth,
                is_active=user.is_active,
                is_verified=user.is_verified,
                first_connection=user.first_connection
            )
            
            if hasattr(user_orm, 'company_id'):
                user_orm.company_id = user.company_id
            
            if hasattr(user_orm, 'role'):
                user_orm.role = user.role
            
            if user.password_hash:
                user_orm.set_password(user.password_hash)
            
            user_orm.save()
        
        return self._to_domain(user_orm)
    
    @transaction.atomic
    def delete(self, user_id) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: The ID of the user to delete
            
        Returns:
            bool: True if the user was deleted, False otherwise
        """
        try:
            user_orm = DjangoUser.objects.get(id=user_id)
            user_orm.delete()
            return True
        except DjangoUser.DoesNotExist:
            return False
    
    def _to_domain(self, user_orm) -> User:
        """
        Convert a Django ORM user to a domain user.
        
        Args:
            user_orm: The Django ORM user to convert
            
        Returns:
            User: The domain user
        """
        company_id = getattr(user_orm, 'company_id', None)
        role = getattr(user_orm, 'role', None)
        
        return User(
            id=user_orm.id,
            email=user_orm.email,
            username=user_orm.username,
            phone_number=user_orm.phone_number,
            first_name=user_orm.first_name,
            last_name=user_orm.last_name,
            date_of_birth=user_orm.date_of_birth,
            is_active=user_orm.is_active,
            is_verified=user_orm.is_verified,
            first_connection=user_orm.first_connection,
            company_id=company_id,
            role=role,
            # We don't include the password hash in the domain model
            password_hash=None
        )


class InvitationRepository(InvitationRepositoryInterface):
    """
    Implementation of the invitation repository interface using Django ORM.
    """
    
    def get_by_id(self, invitation_id) -> Optional[Invitation]:
        """
        Get an invitation by ID.
        
        Args:
            invitation_id: The ID of the invitation to retrieve
            
        Returns:
            Invitation: The invitation with the given ID, or None if not found
        """
        try:
            invitation_orm = InvitationORM.objects.get(id=invitation_id)
            return self._to_domain(invitation_orm)
        except InvitationORM.DoesNotExist:
            return None
    
    def get_by_email(self, email) -> Optional[Invitation]:
        """
        Get an invitation by email.
        
        Args:
            email: The email of the invitation to retrieve
            
        Returns:
            Invitation: The invitation with the given email, or None if not found
        """
        try:
            invitation_orm = InvitationORM.objects.get(email=email)
            return self._to_domain(invitation_orm)
        except InvitationORM.DoesNotExist:
            return None
    
    def get_by_token(self, token) -> Optional[Invitation]:
        """
        Get an invitation by token.
        
        Args:
            token: The token of the invitation to retrieve
            
        Returns:
            Invitation: The invitation with the given token, or None if not found
        """
        try:
            invitation_orm = InvitationORM.objects.get(token=token)
            return self._to_domain(invitation_orm)
        except InvitationORM.DoesNotExist:
            return None
    
    def get_by_sender_id(self, sender_id) -> List[Invitation]:
        """
        Get all invitations sent by a user.
        
        Args:
            sender_id: The ID of the sender
            
        Returns:
            List[Invitation]: A list of invitations sent by the user
        """
        invitation_orms = InvitationORM.objects.filter(sender_id=sender_id)
        return [self._to_domain(invitation_orm) for invitation_orm in invitation_orms]
    
    @transaction.atomic
    def save(self, invitation: Invitation) -> Invitation:
        """
        Save an invitation.
        
        This method creates a new invitation if the invitation doesn't have an ID,
        or updates an existing invitation if the invitation has an ID.
        
        Args:
            invitation: The invitation to save
            
        Returns:
            Invitation: The saved invitation with updated information (e.g., ID if it was a new invitation)
        """
        if invitation.id:
            try:
                invitation_orm = InvitationORM.objects.get(id=invitation.id)
                # Update existing invitation
                invitation_orm.email = invitation.email
                invitation_orm.sender_id = invitation.sender_id
                invitation_orm.token = invitation.token
                invitation_orm.status = invitation.status
                invitation_orm.expires_at = invitation.expires_at
                invitation_orm.save()
            except InvitationORM.DoesNotExist:
                # Create new invitation with existing ID
                invitation_orm = InvitationORM(
                    id=invitation.id,
                    email=invitation.email,
                    sender_id=invitation.sender_id,
                    token=invitation.token,
                    status=invitation.status,
                    expires_at=invitation.expires_at
                )
                invitation_orm.save()
        else:
            # Create new invitation
            invitation_orm = InvitationORM(
                email=invitation.email,
                sender_id=invitation.sender_id,
                token=invitation.token,
                status=invitation.status,
                expires_at=invitation.expires_at
            )
            invitation_orm.save()
        
        return self._to_domain(invitation_orm)
    
    @transaction.atomic
    def delete(self, invitation_id) -> bool:
        """
        Delete an invitation.
        
        Args:
            invitation_id: The ID of the invitation to delete
            
        Returns:
            bool: True if the invitation was deleted, False otherwise
        """
        try:
            invitation_orm = InvitationORM.objects.get(id=invitation_id)
            invitation_orm.delete()
            return True
        except InvitationORM.DoesNotExist:
            return False
    
    def _to_domain(self, invitation_orm) -> Invitation:
        """
        Convert a Django ORM invitation to a domain invitation.
        
        Args:
            invitation_orm: The Django ORM invitation to convert
            
        Returns:
            Invitation: The domain invitation
        """
        return Invitation(
            id=invitation_orm.id,
            email=invitation_orm.email,
            sender_id=invitation_orm.sender_id,
            token=invitation_orm.token,
            status=invitation_orm.status,
            expires_at=invitation_orm.expires_at
        )

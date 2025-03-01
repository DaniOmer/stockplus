"""
Application services for the user application.
This module contains the application services for the user application.
"""

from typing import List, Optional

from builder.modules.user.domain.models import User, Invitation
from builder.modules.user.domain.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    InvitationNotFoundException,
    InvitationExpiredException,
    InvitationAlreadyValidatedException,
    ValidationException
)
from builder.modules.user.application.interfaces import (
    UserRepositoryInterface,
    InvitationRepositoryInterface
)


class UserService:
    """
    User service.

    This class implements the application logic for users. It uses the user repository
    to access and manipulate user data and enforces business rules.
    """

    def __init__(self, user_repository: UserRepositoryInterface):
        """
        Initialize a new UserService instance.

        Args:
            user_repository: The user repository to use
        """
        self.user_repository = user_repository

    def get_user_by_id(self, user_id) -> Optional[User]:
        """
        Get a user by ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            User: The user with the given ID or None if not found
        """
        return self.user_repository.get_by_id(user_id)

    def get_user_by_email(self, email) -> Optional[User]:
        """
        Get a user by email.

        Args:
            email: The email of the user to retrieve

        Returns:
            User: The user with the given email or None if not found
        """
        return self.user_repository.get_by_email(email)

    def get_user_by_phone_number(self, phone_number) -> Optional[User]:
        """
        Get a user by phone number.

        Args:
            phone_number: The phone number of the user to retrieve

        Returns:
            User: The user with the given phone number or None if not found
        """
        return self.user_repository.get_by_phone_number(phone_number)

    def get_user_by_username(self, username) -> Optional[User]:
        """
        Get a user by username.

        Args:
            username: The username of the user to retrieve

        Returns:
            User: The user with the given username or None if not found
        """
        return self.user_repository.get_by_username(username)

    def get_users_by_company(self, company_id) -> List[User]:
        """
        Get all users for a company.

        Args:
            company_id: The ID of the company

        Returns:
            List[User]: A list of users for the company
        """
        return self.user_repository.get_by_company_id(company_id)

    def create_user(self, email=None, phone_number=None, username=None,
                     first_name=None, last_name=None, password=None) -> User:
        """
        Create a new user.

        Args:
            email: The user's email address
            phone_number: The user's phone number
            username: The user's username
            first_name: The user's first name
            last_name: The user's last name
            password: The user's password

        Returns:
            User: The newly created user

        Raises:
            ValidationException: If the user data is invalid
            UserAlreadyExistsException: If a user with the given email or phone number already exists
        """
        # Validate input
        if not email and not phone_number:
            raise ValidationException("Email or phone number is required")

        # Check if user already exists
        if email and self.user_repository.get_by_email(email):
            raise UserAlreadyExistsException(f"User with email {email} already exists")

        if phone_number and self.user_repository.get_by_phone_number(phone_number):
            raise UserAlreadyExistsException(f"User with phone number {phone_number} already exists")

        # Create new user
        user = User(
            email=email,
            phone_number=phone_number,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password_hash=password  # Note: The repository will handle password hashing
        )

        # Save user
        return self.user_repository.save(user)

    def authenticate_user(self, email=None, phone_number=None, password=None) -> Optional[User]:
        """
        Authenticate a user.

        Args:
            email: The user's email address
            phone_number: The user's phone number
            password: The user's password

        Returns:
            User: The authenticated user or None if authentication fails
        """
        # Validate input
        if not email and not phone_number:
            return None

        # Get user
        user = None
        if email:
            user = self.user_repository.get_by_email(email)
        elif phone_number:
            user = self.user_repository.get_by_phone_number(phone_number)

        if not user:
            return None

        # Verify password
        if not self.user_repository.verify_password(user.id, password):
            return None

        return user

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
        # Get user
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")

        # Update password
        return self.user_repository.update_password(user_id, new_password)

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
        # Get user
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")

        # Verify user
        user.verify()

        # Save user
        return self.user_repository.save(user)

    def update_user(self, user_id, email=None, phone_number=None,
                           first_name=None, last_name=None) -> User:
        """
        Update a user's profile.

        Args:
            user_id: The ID of the user to update
            email: The user's new email
            phone_number: The user's new phone number
            first_name: The user's new first name
            last_name: The user's new last name

        Returns:
            User: The updated user

        Raises:
            UserNotFoundException: If the user is not found
        """
        # Get user
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")

        # Update user
        user.update_profile(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )

        # Save user
        return self.user_repository.save(user)

    def assign_user_to_company(self, user_id, company_id, role) -> User:
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
        # Get user
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")

        # Assign user to company
        user.assign_to_company(company_id, role)

        # Save user
        return self.user_repository.save(user)

    def remove_user_from_company(self, user_id) -> User:
        """
        Remove a user from their company.

        Args:
            user_id: The ID of the user to remove from their company

        Returns:
            User: The updated user

        Raises:
            UserNotFoundException: If the user is not found
        """
        # Get user
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")

        # Remove user from company
        user.remove_from_company()

        # Save user
        return self.user_repository.save(user)

    def deactivate_user(self, user_id) -> User:
        """
        Deactivate a user.

        Args:
            user_id: The ID of the user to deactivate

        Returns:
            User: The deactivated user

        Raises:
            UserNotFoundException: If the user is not found
        """
        # Get user
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")

        # Deactivate user
        user.deactivate()

        # Save user
        return self.user_repository.save(user)

    def activate_user(self, user_id) -> User:
        """
        Activate a user.

        Args:
            user_id: The ID of the user to activate

        Returns:
            User: The activated user

        Raises:
            UserNotFoundException: If the user is not found
        """
        # Get user
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")

        # Activate user
        user.activate()

        # Save user
        return self.user_repository.save(user)

    def delete_user(self, user_id) -> bool:
        """
        Delete a user.

        Args:
            user_id: The ID of the user to delete

        Returns:
            bool: True if the user was deleted, False otherwise
        """
        return self.user_repository.delete(user_id)


class InvitationService:
    """
    Invitation service.

    This class implements the application logic for invitations. It uses the invitation repository
    to access and manipulate invitation data and enforces business rules.
    """

    def __init__(self, invitation_repository: InvitationRepositoryInterface,
                 user_repository: UserRepositoryInterface):
        """
        Initialize a new InvitationService instance.

        Args:
            invitation_repository: The invitation repository to use
            user_repository: The user repository to use
        """
        self.invitation_repository = invitation_repository
        self.user_repository = user_repository

    def get_invitation_by_id(self, invitation_id) -> Optional[Invitation]:
        """
        Get an invitation by ID.

        Args:
            invitation_id: The ID of the invitation to retrieve

        Returns:
            Invitation: The invitation with the given ID or None if not found
        """
        return self.invitation_repository.get_by_id(invitation_id)

    def get_invitation_by_email(self, email) -> Optional[Invitation]:
        """
        Get an invitation by email.

        Args:
            email: The email of the invitation to retrieve

        Returns:
            Invitation: The invitation with the given email or None if not found
        """
        return self.invitation_repository.get_by_email(email)

    def get_invitation_by_token(self, token) -> Optional[Invitation]:
        """
        Get an invitation by token.

        Args:
            token: The token of the invitation to retrieve

        Returns:
            Invitation: The invitation with the given token or None if not found
        """
        return self.invitation_repository.get_by_token(token)

    def get_invitations_by_sender(self, sender_id) -> List[Invitation]:
        """
        Get all invitations sent by a user.

        Args:
            sender_id: The ID of the sender

        Returns:
            List[Invitation]: A list of invitations sent by the user
        """
        return self.invitation_repository.get_by_sender_id(sender_id)

    def create_invitation(self, email, sender_id) -> Invitation:
        """
        Create a new invitation.

        Args:
            email: The email of the invitee
            sender_id: The ID of the sender

        Returns:
            Invitation: The newly created invitation

        Raises:
            ValidationException: If the invitation data is invalid
            UserAlreadyExistsException: If a user with the given email already exists
        """
        # Validate input
        if not email:
            raise ValidationException("Email is required")

        # Check if user already exists
        if self.user_repository.get_by_email(email):
            raise UserAlreadyExistsException(f"User with email {email} already exists")

        # Check if invitation already exists
        existing_invitation = self.invitation_repository.get_by_email(email)
        if existing_invitation:
            # If the invitation has expired, delete it and create a new one
            if not existing_invitation.is_valid():
                self.invitation_repository.delete(existing_invitation.id)
            else:
                # If the invitation is still valid, return it
                return existing_invitation

        # Create new invitation
        invitation = Invitation(
            email=email,
            sender_id=sender_id
        )

        # Save invitation
        return self.invitation_repository.save(invitation)

    def validate_invitation(self, token) -> Invitation:
        """
        Validate an invitation.

        Args:
            token: The token of the invitation to validate

        Returns:
            Invitation: The validated invitation

        Raises:
            InvitationNotFoundException: If the invitation is not found
            InvitationExpiredException: If the invitation has expired
            InvitationAlreadyValidatedException: If the invitation has already been validated
        """
        # Get invitation
        invitation = self.invitation_repository.get_by_token(token)
        if not invitation:
            raise InvitationNotFoundException(f"Invitation with token {token} not found")

        # Check if invitation is valid
        if not invitation.is_valid():
            raise InvitationExpiredException("Invitation has expired")

        # Check if invitation has already been validated
        if invitation.status == 'VALIDATED':
            raise InvitationAlreadyValidatedException("Invitation has already been validated")

        # Validate invitation
        invitation.mark_as_validated()

        # Save invitation
        return self.invitation_repository.save(invitation)

    def delete_invitation(self, invitation_id) -> bool:
        """
        Delete an invitation.

        Args:
            invitation_id: The ID of the invitation to delete

        Returns:
            bool: True if the invitation was deleted, False otherwise
        """
        return self.invitation_repository.delete(invitation_id)

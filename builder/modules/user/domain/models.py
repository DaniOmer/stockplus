"""
Domain models for the user application.
This module contains the domain models for the user application.
"""

from datetime import datetime, timedelta
import uuid


class User:
    """
    User domain model.
    
    This class represents a user in the system, with all its business rules and behaviors.
    It is independent of any framework or infrastructure concerns.
    """
    
    def __init__(self, id=None, email=None, username=None, phone_number=None,
                 first_name=None, last_name=None, date_of_birth=None,
                 is_active=True, is_verified=False, first_connection=None,
                 company_id=None, role=None, password_hash=None):
        """
        Initialize a new User instance.
        
        Args:
            id: The user's unique identifier
            email: The user's email address
            username: The user's username
            phone_number: The user's phone number
            first_name: The user's first name
            last_name: The user's last name
            date_of_birth: The user's date of birth
            is_active: Whether the user is active
            is_verified: Whether the user is verified
            first_connection: The date and time of the user's first connection
            company_id: The ID of the company the user belongs to
            role: The user's role in the company
            password_hash: The user's hashed password
        """
        self.id = id
        self.email = email
        self.username = username
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.is_active = is_active
        self.is_verified = is_verified
        self.first_connection = first_connection
        self.company_id = company_id
        self.role = role
        self.password_hash = password_hash
    
    @property
    def fullname(self):
        """
        Get the user's full name.
        
        Returns:
            str: The user's full name
        """
        return f"{self.first_name or ''} {self.last_name or ''}".strip()
    
    def verify(self):
        """
        Mark the user as verified.
        """
        self.is_verified = True
    
    def activate(self):
        """
        Activate the user.
        """
        self.is_active = True
    
    def deactivate(self):
        """
        Deactivate the user.
        """
        self.is_active = False
    
    def update_profile(self, first_name=None, last_name=None, username=None, date_of_birth=None):
        """
        Update the user's profile information.
        
        Args:
            first_name: The user's new first name
            last_name: The user's new last name
            username: The user's new username
            date_of_birth: The user's new date of birth
        """
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if username is not None:
            self.username = username
        if date_of_birth is not None:
            self.date_of_birth = date_of_birth
    
    def assign_to_company(self, company_id, role):
        """
        Assign the user to a company with a specific role.
        
        Args:
            company_id: The ID of the company
            role: The user's role in the company
        """
        self.company_id = company_id
        self.role = role
    
    def remove_from_company(self):
        """
        Remove the user from their company.
        """
        self.company_id = None
        self.role = None
    
    def record_first_connection(self):
        """
        Record the user's first connection.
        """
        if not self.first_connection:
            self.first_connection = datetime.now()


class Invitation:
    """
    Invitation domain model.
    
    This class represents an invitation to join the system.
    """
    
    def __init__(self, id=None, email=None, sender_id=None, token=None,
                 status='PENDING', expires_at=None):
        """
        Initialize a new Invitation instance.
        
        Args:
            id: The invitation's unique identifier
            email: The email address of the invitee
            sender_id: The ID of the user who sent the invitation
            token: The invitation token
            status: The status of the invitation
            expires_at: The date and time when the invitation expires
        """
        self.id = id
        self.email = email
        self.sender_id = sender_id
        self.token = token or str(uuid.uuid4())
        self.status = status
        self.expires_at = expires_at or (datetime.now() + timedelta(hours=48))
    
    def mark_as_validated(self):
        """
        Mark the invitation as validated.
        """
        self.status = 'VALIDATED'
    
    def mark_as_expired(self):
        """
        Mark the invitation as expired.
        """
        self.status = 'EXPIRED'
    
    def is_valid(self):
        """
        Check if the invitation is valid.
        
        Returns:
            bool: True if the invitation is valid, False otherwise
        """
        return self.status == 'PENDING' and datetime.now() < self.expires_at

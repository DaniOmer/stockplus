"""
Data Transfer Objects (DTOs) for the user application.
This module contains the DTOs for the user application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, field_validator, EmailStr, StringConstraints
from typing_extensions import Annotated, Optional

# Validation patterns
NAME_PATTERN = r'^[a-zA-Z\s\-\']+$'
PHONE_PATTERN = r'^\+?[0-9]\d{1,14}$'
# Simplified password pattern without lookahead
PASSWORD_PATTERN = r'^[A-Za-z\d@$!%*#?&,;]{7,}$'

TOKEN_PATTERN = r'^[a-zA-Z0-9-_]+$'

NameStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=100,
        pattern=NAME_PATTERN
    )
]

PhoneStr = Annotated[
    str,
    StringConstraints(
        pattern=PHONE_PATTERN
    )
]

PasswordStr = Annotated[
    str,
    StringConstraints(
        min_length=8,
        pattern=PASSWORD_PATTERN
    )
]

TokenStr = Annotated[
    str,
    StringConstraints(
        pattern=TOKEN_PATTERN,
        min_length=1,
        max_length=255
    )
]

class UserBaseDTO(BaseModel):
    """
    Base DTO for user data.
    Contains common validation rules for user data.
    """
    email: EmailStr = Field(..., description="User's email address")
    first_name: NameStr = Field(..., description="User's first name")
    last_name: NameStr = Field(..., description="User's last name")
    phone_number: Optional[PhoneStr] = Field(None, description="User's phone number")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }

class UserCreateDTO(UserBaseDTO):
    """
    DTO for creating a new user.
    """
    password: PasswordStr = Field(..., description="User's password")
    
    @field_validator('password')
    def validate_password_strength(cls, v):
        """Validate that password contains at least one letter and one digit."""
        has_letter = any(c.isalpha() for c in v)
        has_digit = any(c.isdigit() for c in v)
        if not (has_letter and has_digit):
            raise ValueError('Password must contain at least one letter and one digit')
        return v
    
class UserLoginDTO(BaseModel):
    """
    DTO for user login.
    """
    email: Optional[EmailStr] = Field(None, description="User's email address")
    phone_number: Optional[PhoneStr] = Field(None, description="User's phone number")
    password: PasswordStr = Field(..., description="User's password")

    @field_validator('email', 'phone_number')
    def validate_credentials(cls, v, values):
        if not v and not values.get('email') and not values.get('phone_number'):
            raise ValueError("Either email or phone_number must be provided")
        return v

class UserUpdateDTO(UserBaseDTO):
    """
    DTO for updating user information.
    """
    email: Optional[EmailStr] = Field(None, description="User's email address")
    first_name: Optional[NameStr] = Field(None, description="User's first name")
    last_name: Optional[NameStr] = Field(None, description="User's last name")
    phone_number: Optional[PhoneStr] = Field(None, description="User's phone number")
    # country: Optional[str] = Field(None, min_length=2, max_length=2, description="User's country code (ISO 2)")

class UserPasswordUpdateDTO(BaseModel):
    """
    DTO for updating user password.
    """
    old_password: PasswordStr = Field(..., description="Current password")
    new_password: PasswordStr = Field(..., description="New password")

    @field_validator('new_password')
    def validate_new_password(cls, v, values):
        """Validate that new password is different from old password and has required strength."""
        # Check that passwords are different
        if 'old_password' in values and v == values['old_password']:
            raise ValueError('New password must be different from current password')
        
        # Check password strength
        has_letter = any(c.isalpha() for c in v)
        has_digit = any(c.isdigit() for c in v)
        if not (has_letter and has_digit):
            raise ValueError('Password must contain at least one letter and one digit')
            
        return v

    model_config = {
        "extra": "forbid",
    }
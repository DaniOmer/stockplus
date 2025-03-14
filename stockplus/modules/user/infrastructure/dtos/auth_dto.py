"""
Data Transfer Objects (DTOs) for user authentication.
This module contains the DTOs for user authentication.
"""

from pydantic import BaseModel, Field, field_validator, EmailStr, StringConstraints
from typing_extensions import Annotated

# Validation patterns
TOKEN_PATTERN = r'^[a-zA-Z0-9-_]+$'
# Simplified password pattern without lookahead
PASSWORD_PATTERN = r'^[A-Za-z\d@$!%*#?&,;]{7,}$'
PHONE_PATTERN = r'^\+?[1-9]\d{1,14}$'

TokenStr = Annotated[
    str,
    StringConstraints(
        pattern=TOKEN_PATTERN,
        min_length=1,
        max_length=255
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

class EmailVerifyDTO(BaseModel):
    """
    DTO for email verification.
    """
    token: TokenStr = Field(..., description="Verification token")

    model_config = {
        "extra": "forbid",
    }

class ResendVerificationEmailDTO(BaseModel):
    """
    DTO for resending verification email.
    """
    email: EmailStr = Field(..., description="User's email address")
    verification_method: str = Field(
        default="email",
        pattern="^(email|sms)$",
        description="Verification method (email or sms)"
    )

    model_config = {
        "extra": "forbid",
    }

class PasswordResetRequestDTO(BaseModel):
    """
    DTO for password reset request.
    """
    email: EmailStr = Field(..., description="User's email address")

    model_config = {
        "extra": "forbid",
    }

class PasswordResetConfirmDTO(BaseModel):
    """
    DTO for password reset confirmation.
    """
    token: TokenStr = Field(..., description="Reset token")
    new_password: PasswordStr = Field(..., description="New password")

    @field_validator('new_password')
    def validate_password_strength(cls, v):
        """Validate that password contains at least one letter and one digit."""
        has_letter = any(c.isalpha() for c in v)
        has_digit = any(c.isdigit() for c in v)
        if not (has_letter and has_digit):
            raise ValueError('Password must contain at least one letter and one digit')
        return v

    model_config = {
        "extra": "forbid",
    }

class PasswordUpdateDTO(BaseModel):
    """
    DTO for updating password.
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
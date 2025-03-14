"""
Data Transfer Objects (DTOs) for the user application.
This module contains the DTOs for the user application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, field_validator, EmailStr, StringConstraints
from typing_extensions import Annotated, Optional

# Validation patterns
NAME_PATTERN = r'^[a-zA-Z\s\-\']+$'
PHONE_PATTERN = r'^\+?[1-9]\d{1,14}$'
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
    # country: str = Field(..., min_length=2, max_length=2, description="User's country code (ISO 2)")
    
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
    country: Optional[str] = Field(None, min_length=2, max_length=2, description="User's country code (ISO 2)")

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

# class UserVerificationDTO(BaseModel):
#     """
#     DTO for user verification.
#     """
#     token: str = Field(..., description="Verification token")
    
#     model_config = {
#         "extra": "forbid",  # Forbid extra fields to prevent data injection
#     }

# class PasswordResetRequestDTO(BaseModel):
#     """
#     DTO for password reset request.
#     """
#     email: Optional[EmailStr] = Field(None, description="User's email address")
#     phone_number: Optional[PhoneStr] = Field(None, description="User's phone number")
    
#     @field_validator('email', 'phone_number')
#     def validate_reset_method(cls, v, info):
#         field_name = info.field_name
#         return v
    
#     model_config = {
#         "extra": "forbid",  # Forbid extra fields to prevent data injection
#     }

# class PasswordResetConfirmDTO(BaseModel):
#     """
#     DTO for password reset confirmation.
#     """
#     token: TokenStr = Field(..., description="Reset token")
#     new_password: str = Field(
#         ...,
#         min_length=8,
#         description="New password"
#     )

#     @field_validator('new_password')
#     def validate_password_strength(cls, v):
#         """Validate that the password meets strength requirements."""
#         has_letter = any(c.isalpha() for c in v)
#         has_digit = any(c.isdigit() for c in v)
#         valid_chars = all(c.isalnum() or c in '@$!%*#?&' for c in v)
        
#         if not has_letter:
#             raise ValueError('Password must contain at least one letter')
#         if not has_digit:
#             raise ValueError('Password must contain at least one digit')
#         if not valid_chars:
#             raise ValueError('Password contains invalid characters. Only alphanumeric and @$!%*#?& are allowed')
            
#         return v

#     model_config = {
#         "extra": "forbid",
#     }

# class EmailVerifyDTO(BaseModel):
#     """
#     DTO for email verification.
#     """
#     token: TokenStr = Field(..., description="Verification token")

# class ResendVerificationEmailDTO(BaseModel):
#     """
#     DTO for resending verification email.
#     """
#     email: EmailStr = Field(..., description="User's email address")
#     verification_method: str = Field(
#         default="email",
#         pattern="^(email|sms)$",
#         description="Verification method (email or sms)"
#     )

# class PasswordResetRequestDTO(BaseModel):
#     """
#     DTO for password reset request.
#     """
#     email: EmailStr = Field(..., description="User's email address")

# class PasswordResetConfirmDTO(BaseModel):
#     """
#     DTO for password reset confirmation.
#     """
#     token: TokenStr = Field(..., description="Reset token")
#     new_password: str = Field(
#         ...,
#         min_length=8,
#         description="New password"
#     )

#     @field_validator('new_password')
#     def validate_password_strength(cls, v):
#         """Validate that the password meets strength requirements."""
#         has_letter = any(c.isalpha() for c in v)
#         has_digit = any(c.isdigit() for c in v)
#         valid_chars = all(c.isalnum() or c in '@$!%*#?&' for c in v)
        
#         if not has_letter:
#             raise ValueError('Password must contain at least one letter')
#         if not has_digit:
#             raise ValueError('Password must contain at least one digit')
#         if not valid_chars:
#             raise ValueError('Password contains invalid characters. Only alphanumeric and @$!%*#?& are allowed')
            
#         return v

#     model_config = {
#         "extra": "forbid",
#     } 
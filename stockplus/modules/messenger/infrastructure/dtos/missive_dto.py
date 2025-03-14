"""
Data Transfer Objects (DTOs) for the messenger application.
This module contains the DTOs for the messenger application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, field_validator, EmailStr, HttpUrl
from typing import Optional, Literal
from enum import Enum


class ModeEnum(str, Enum):
    """
    Enum for message mode.
    """
    EMAIL = 'EMAIL'
    SMS = 'SMS'
    POSTAL = 'POSTAL'
    POSTALAR = 'POSTALAR'
    WEB = 'WEB'


class StatusEnum(str, Enum):
    """
    Enum for message status.
    """
    PREPARE = 'PREPARE'
    SENT = 'SENT'
    ERROR = 'ERROR'


class MissiveBaseDTO(BaseModel):
    """
    Base DTO for missive data.
    Contains common validation rules for missive data.
    """
    
    # Required fields
    mode: ModeEnum = Field(ModeEnum.EMAIL, description="Message mode (EMAIL, SMS, POSTAL, POSTALAR, WEB)")
    target: str = Field(..., min_length=1, max_length=255, description="Target recipient (email, phone number, etc.)")
    subject: str = Field(..., min_length=1, max_length=255, description="Message subject")
    
    # Optional fields
    status: StatusEnum = Field(StatusEnum.PREPARE, description="Message status (PREPARE, SENT, ERROR)")
    name: Optional[str] = Field(None, max_length=100, description="Message name or identifier")
    sender: Optional[str] = Field(None, max_length=255, description="Sender address")
    reply: Optional[str] = Field(None, max_length=255, description="Reply-to address")
    service: Optional[str] = Field(None, max_length=100, description="Service identifier")
    denomination: Optional[str] = Field(None, max_length=255, description="Recipient organization name")
    last_name: Optional[str] = Field(None, max_length=100, description="Recipient last name")
    first_name: Optional[str] = Field(None, max_length=100, description="Recipient first name")
    header_html: Optional[str] = Field(None, description="HTML header content")
    footer_html: Optional[str] = Field(None, description="HTML footer content")
    template: Optional[str] = Field(None, max_length=255, description="Template identifier")
    html: Optional[str] = Field(None, description="HTML content")
    txt: Optional[str] = Field(None, description="Plain text content")
    content_type: Optional[str] = Field(None, max_length=100, description="Content MIME type")
    object_id: Optional[int] = Field(None, description="Related object ID")
    backend: Optional[str] = Field(None, max_length=100, description="Backend service identifier")
    msg_id: Optional[str] = Field(None, max_length=255, description="Message ID from the backend")
    response: Optional[str] = Field(None, description="Backend response")
    partner_id: Optional[str] = Field(None, max_length=100, description="Partner identifier")
    code_error: Optional[str] = Field(None, max_length=100, description="Error code")
    trace: Optional[str] = Field(None, description="Error trace")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('sender', 'reply')
    def validate_email_fields(cls, v, info):
        field_name = info.field_name
        if v and info.data.get('mode') == ModeEnum.EMAIL:
            # Simple validation for email format
            if '@' not in v:
                raise ValueError(f'{field_name} must be a valid email address for EMAIL mode')
        return v
    
    @field_validator('target')
    def validate_target(cls, v, info):
        mode = info.data.get('mode')
        if mode == ModeEnum.EMAIL:
            # Simple validation for email format
            if '@' not in v:
                raise ValueError('Target must be a valid email address for EMAIL mode')
        elif mode == ModeEnum.SMS:
            # Simple validation for phone number format
            if not v.replace('+', '').isdigit():
                raise ValueError('Target must be a valid phone number for SMS mode')
        return v


class MissiveCreateDTO(MissiveBaseDTO):
    """
    DTO for creating a new missive.
    Inherits validation rules from MissiveBaseDTO.
    """
    pass


class MissiveUpdateDTO(MissiveBaseDTO):
    """
    DTO for updating missive information.
    """
    pass


class MissivePartialUpdateDTO(MissiveBaseDTO):
    """
    DTO for partially updating missive information.
    All fields are optional.
    """
    mode: Optional[ModeEnum] = Field(None, description="Message mode (EMAIL, SMS, POSTAL, POSTALAR, WEB)")
    target: Optional[str] = Field(None, min_length=1, max_length=255, description="Target recipient (email, phone number, etc.)")
    subject: Optional[str] = Field(None, min_length=1, max_length=255, description="Message subject")


class MissiveStatusUpdateDTO(BaseModel):
    """
    DTO for updating missive status.
    """
    status: StatusEnum = Field(..., description="New status (PREPARE, SENT, ERROR)")
    code_error: Optional[str] = Field(None, max_length=100, description="Error code (required if status is ERROR)")
    trace: Optional[str] = Field(None, description="Error trace (optional if status is ERROR)")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('code_error')
    def validate_code_error(cls, v, info):
        if info.data.get('status') == StatusEnum.ERROR and not v:
            raise ValueError('Error code is required when status is ERROR')
        return v


class EmailMissiveDTO(MissiveBaseDTO):
    """
    Specialized DTO for email missives.
    """
    mode: Literal[ModeEnum.EMAIL] = Field(ModeEnum.EMAIL, description="Email mode")
    sender: EmailStr = Field(..., description="Sender email address")
    target: EmailStr = Field(..., description="Recipient email address")
    reply: Optional[EmailStr] = Field(None, description="Reply-to email address")
    html: Optional[str] = Field(None, description="HTML content")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class SMSMissiveDTO(MissiveBaseDTO):
    """
    Specialized DTO for SMS missives.
    """
    mode: Literal[ModeEnum.SMS] = Field(ModeEnum.SMS, description="SMS mode")
    txt: str = Field(..., max_length=1600, description="SMS text content")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('txt')
    def validate_txt_length(cls, v):
        if len(v) > 1600:
            raise ValueError('SMS text content cannot exceed 1600 characters')
        return v


class WebMissiveDTO(MissiveBaseDTO):
    """
    Specialized DTO for web missives.
    """
    mode: Literal[ModeEnum.WEB] = Field(ModeEnum.WEB, description="Web mode")
    html: str = Field(..., description="HTML content")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class MissiveTemplateDTO(BaseModel):
    """
    DTO for missive templates.
    """
    template_id: str = Field(..., min_length=1, max_length=100, description="Template identifier")
    context: dict = Field(..., description="Template context variables")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }

"""
Avatar DTOs for the user module.
This module contains the DTOs for avatar operations.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional

class AvatarUploadDTO(BaseModel):
    """
    DTO for avatar upload.
    """
    signature: str = Field(..., description="HMAC signature for secure upload")
    timestamp: int = Field(..., description="Timestamp when the signature was generated")
    
    @validator('timestamp')
    def timestamp_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Timestamp must be positive')
        return v

class AvatarUrlDTO(BaseModel):
    """
    DTO for avatar URL.
    """
    url: str = Field(..., description="Signed URL for accessing the avatar")
    expires_at: int = Field(..., description="Timestamp when the URL expires")

class AvatarResponseDTO(BaseModel):
    """
    DTO for avatar response.
    """
    avatar_url: Optional[str] = Field(None, description="URL of the avatar")
    message: str = Field(..., description="Response message")

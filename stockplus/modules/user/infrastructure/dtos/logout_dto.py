"""
Data Transfer Objects (DTOs) for user logout.
This module contains the DTOs for user logout.
"""

from pydantic import BaseModel, Field, StringConstraints
from typing_extensions import Annotated, Optional

# Validation patterns
TOKEN_PATTERN = r'^[a-zA-Z0-9-_]+$'

TokenStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=255
    )
]

class LogoutDTO(BaseModel):
    """
    DTO for user logout.
    """
    refresh_token: TokenStr = Field(..., description="Refresh token to blacklist")

    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }

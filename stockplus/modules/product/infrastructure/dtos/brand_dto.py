"""
Data Transfer Objects (DTOs) for the brand application.
This module contains the DTOs for the brand application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, StringConstraints, HttpUrl
from typing import Optional
from typing_extensions import Annotated
from uuid import UUID


# Type annotations
BrandNameStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=100
    )
]


class BrandBaseDTO(BaseModel):
    """
    Base DTO for brand data.
    Contains common validation rules for brand data.
    """
    
    # Required fields
    name: BrandNameStr = Field(..., description="Brand name")
    company_id: int = Field(..., gt=0, description="Company ID that owns this brand")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    description: Optional[str] = Field(None, max_length=500, description="Brand description")
    logo_url: Optional[str] = Field(None, description="URL to brand logo")
    is_active: Optional[bool] = Field(True, description="Whether the brand is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class BrandCreateDTO(BrandBaseDTO):
    """
    DTO for creating a new brand.
    Inherits validation rules from BrandBaseDTO.
    """
    pass


class BrandUpdateDTO(BrandBaseDTO):
    """
    DTO for updating brand information.
    """
    pass


class BrandPartialUpdateDTO(BrandBaseDTO):
    """
    DTO for partially updating brand information.
    All fields are optional.
    """
    name: Optional[BrandNameStr] = Field(None, description="Brand name")
    company_id: Optional[int] = Field(None, gt=0, description="Company ID that owns this brand")


class BrandLogoUpdateDTO(BaseModel):
    """
    DTO for updating brand logo.
    """
    
    logo_url: str = Field(..., description="URL to brand logo")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }

"""
Data Transfer Objects (DTOs) for the product feature application.
This module contains the DTOs for the product feature application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, StringConstraints
from typing import Optional
from typing_extensions import Annotated
from uuid import UUID


# Type annotations
FeatureNameStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=100
    )
]


class ProductFeatureBaseDTO(BaseModel):
    """
    Base DTO for product feature data.
    Contains common validation rules for product feature data.
    """
    
    # Required fields
    name: FeatureNameStr = Field(..., description="Feature name")
    product_id: int = Field(..., gt=0, description="Product ID this feature belongs to")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    description: Optional[str] = Field(None, max_length=500, description="Feature description")
    is_active: Optional[bool] = Field(True, description="Whether the feature is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class ProductFeatureCreateDTO(ProductFeatureBaseDTO):
    """
    DTO for creating a new product feature.
    Inherits validation rules from ProductFeatureBaseDTO.
    """
    pass


class ProductFeatureUpdateDTO(ProductFeatureBaseDTO):
    """
    DTO for updating product feature information.
    """
    pass


class ProductFeaturePartialUpdateDTO(ProductFeatureBaseDTO):
    """
    DTO for partially updating product feature information.
    All fields are optional.
    """
    name: Optional[FeatureNameStr] = Field(None, description="Feature name")
    product_id: Optional[int] = Field(None, gt=0, description="Product ID this feature belongs to")


class ProductFeatureBulkCreateDTO(BaseModel):
    """
    DTO for creating multiple product features at once.
    """
    
    product_id: int = Field(..., gt=0, description="Product ID these features belong to")
    features: list[dict] = Field(..., min_items=1, description="List of features to create")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }

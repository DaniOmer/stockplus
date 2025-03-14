"""
Data Transfer Objects (DTOs) for the product category application.
This module contains the DTOs for the product category application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, StringConstraints
from typing import Optional, List
from typing_extensions import Annotated
from uuid import UUID


# Type annotations
CategoryNameStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=100
    )
]


class ProductCategoryBaseDTO(BaseModel):
    """
    Base DTO for product category data.
    Contains common validation rules for product category data.
    """
    
    # Required fields
    name: CategoryNameStr = Field(..., description="Category name")
    company_id: int = Field(..., gt=0, description="Company ID that owns this category")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    description: Optional[str] = Field(None, max_length=500, description="Category description")
    parent_id: Optional[int] = Field(None, gt=0, description="Parent category ID")
    is_active: Optional[bool] = Field(True, description="Whether the category is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class ProductCategoryCreateDTO(ProductCategoryBaseDTO):
    """
    DTO for creating a new product category.
    Inherits validation rules from ProductCategoryBaseDTO.
    """
    pass


class ProductCategoryUpdateDTO(ProductCategoryBaseDTO):
    """
    DTO for updating product category information.
    """
    pass


class ProductCategoryPartialUpdateDTO(ProductCategoryBaseDTO):
    """
    DTO for partially updating product category information.
    All fields are optional.
    """
    name: Optional[CategoryNameStr] = Field(None, description="Category name")
    company_id: Optional[int] = Field(None, gt=0, description="Company ID that owns this category")


class ProductCategoryTreeDTO(BaseModel):
    """
    DTO for representing a product category tree.
    """
    
    id: int = Field(..., description="Category ID")
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    name: str = Field(..., description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    is_active: bool = Field(..., description="Whether the category is active")
    children: List["ProductCategoryTreeDTO"] = Field([], description="Child categories")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


# Update forward reference for nested model
ProductCategoryTreeDTO.model_rebuild()

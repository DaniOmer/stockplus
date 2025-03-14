"""
Data Transfer Objects (DTOs) for the product variant application.
This module contains the DTOs for the product variant application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, field_validator, StringConstraints
from typing import Optional
from typing_extensions import Annotated
from uuid import UUID


# Type annotations
VariantNameStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=100
    )
]

SKUStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=50
    )
]


class ProductVariantBaseDTO(BaseModel):
    """
    Base DTO for product variant data.
    Contains common validation rules for product variant data.
    """
    
    # Required fields
    product_id: int = Field(..., gt=0, description="Product ID this variant belongs to")
    price: float = Field(..., ge=0, description="Selling price")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    name: Optional[str] = Field(None, max_length=100, description="Variant name")
    color: Optional[str] = Field(None, max_length=50, description="Variant color")
    size: Optional[str] = Field(None, max_length=50, description="Variant size")
    buy_price: Optional[float] = Field(None, ge=0, description="Purchase price")
    sku: Optional[str] = Field(None, max_length=50, description="Stock Keeping Unit")
    is_active: Optional[bool] = Field(True, description="Whether the variant is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('price', 'buy_price')
    def validate_price(cls, v, info):
        field_name = info.field_name
        if v is not None and v < 0:
            raise ValueError(f'{field_name} must be non-negative')
        return v


class ProductVariantCreateDTO(ProductVariantBaseDTO):
    """
    DTO for creating a new product variant.
    Inherits validation rules from ProductVariantBaseDTO.
    """
    pass


class ProductVariantUpdateDTO(ProductVariantBaseDTO):
    """
    DTO for updating product variant information.
    """
    pass


class ProductVariantPartialUpdateDTO(ProductVariantBaseDTO):
    """
    DTO for partially updating product variant information.
    All fields are optional.
    """
    product_id: Optional[int] = Field(None, gt=0, description="Product ID this variant belongs to")
    price: Optional[float] = Field(None, ge=0, description="Selling price")


class ProductVariantPriceUpdateDTO(BaseModel):
    """
    DTO for updating product variant prices.
    """
    
    price: float = Field(..., ge=0, description="New selling price")
    buy_price: Optional[float] = Field(None, ge=0, description="New purchase price")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }

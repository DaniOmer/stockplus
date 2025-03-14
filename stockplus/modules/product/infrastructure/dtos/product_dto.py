"""
Data Transfer Objects (DTOs) for the product application.
This module contains the DTOs for the product application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, field_validator, StringConstraints, HttpUrl
from typing import List, Optional
from typing_extensions import Annotated
from uuid import UUID


# Type annotations
ProductNameStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=255
    )
]

BarcodeStr = Annotated[
    str,
    StringConstraints(
        pattern=r'^[0-9]{8,14}$'
    )
]


class ProductBaseDTO(BaseModel):
    """
    Base DTO for product data.
    Contains common validation rules for product data.
    """
    
    # Required fields
    name: ProductNameStr = Field(..., description="Product name")
    company_id: int = Field(..., gt=0, description="Company ID that owns this product")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    description: Optional[str] = Field(None, max_length=2000, description="Product description")
    barcode: Optional[str] = Field(None, description="Product barcode")
    barcode_image: Optional[str] = Field(None, description="URL to barcode image")
    stock: Optional[int] = Field(0, ge=0, description="Current stock quantity")
    low_stock_threshold: Optional[int] = Field(5, ge=0, description="Low stock threshold")
    brand_id: Optional[int] = Field(None, gt=0, description="Brand ID")
    category_id: Optional[int] = Field(None, gt=0, description="Category ID")
    is_active: Optional[bool] = Field(True, description="Whether the product is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('barcode')
    def validate_barcode(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('Barcode must contain only digits')
        if v is not None and not (8 <= len(v) <= 14):
            raise ValueError('Barcode must be between 8 and 14 digits')
        return v


class ProductCreateDTO(ProductBaseDTO):
    """
    DTO for creating a new product.
    Inherits validation rules from ProductBaseDTO.
    """
    pass


class ProductUpdateDTO(ProductBaseDTO):
    """
    DTO for updating product information.
    """
    pass


class ProductPartialUpdateDTO(ProductBaseDTO):
    """
    DTO for partially updating product information.
    All fields are optional.
    """
    name: Optional[ProductNameStr] = Field(None, description="Product name")
    company_id: Optional[int] = Field(None, gt=0, description="Company ID that owns this product")


class ProductStockUpdateDTO(BaseModel):
    """
    DTO for updating product stock.
    """
    
    stock: int = Field(..., ge=0, description="New stock quantity")
    low_stock_threshold: Optional[int] = Field(None, ge=0, description="New low stock threshold")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class ProductBarcodeUpdateDTO(BaseModel):
    """
    DTO for updating product barcode.
    """
    
    barcode: str = Field(..., description="New barcode")
    generate_image: Optional[bool] = Field(True, description="Whether to generate a barcode image")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('barcode')
    def validate_barcode(cls, v):
        if not v.isdigit():
            raise ValueError('Barcode must contain only digits')
        if not (8 <= len(v) <= 14):
            raise ValueError('Barcode must be between 8 and 14 digits')
        return v

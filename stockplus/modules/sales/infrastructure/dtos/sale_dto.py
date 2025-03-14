"""
Data Transfer Objects (DTOs) for the sales application.
This module contains the DTOs for the sales application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, field_validator, StringConstraints
from typing import List, Optional
from typing_extensions import Annotated
from uuid import UUID
from datetime import datetime
from decimal import Decimal


# Type annotations
InvoiceNumberStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=50
    )
]


class SaleItemBaseDTO(BaseModel):
    """
    Base DTO for sale item data.
    Contains common validation rules for sale item data.
    """
    
    # Required fields
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity")
    unit_price: Decimal = Field(..., ge=0, description="Unit price")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    product_variant_id: Optional[int] = Field(None, gt=0, description="Product variant ID")
    discount: Optional[Decimal] = Field(Decimal('0.00'), ge=0, description="Discount amount")
    total_price: Optional[Decimal] = Field(None, ge=0, description="Total price")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than zero')
        return v
    
    @field_validator('unit_price', 'discount', 'total_price')
    def validate_price(cls, v, info):
        field_name = info.field_name
        if v is not None and v < 0:
            raise ValueError(f'{field_name} must be non-negative')
        return v


class SaleBaseDTO(BaseModel):
    """
    Base DTO for sale data.
    Contains common validation rules for sale data.
    """
    
    # Required fields
    company_id: int = Field(..., gt=0, description="Company ID")
    items: List[SaleItemBaseDTO] = Field(..., min_items=1, description="Sale items")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    invoice_number: Optional[str] = Field(None, max_length=50, description="Invoice number")
    date: Optional[datetime] = Field(None, description="Sale date")
    total_amount: Optional[Decimal] = Field(None, ge=0, description="Total amount")
    payment_method: Optional[str] = Field("cash", max_length=50, description="Payment method")
    point_of_sale_id: Optional[int] = Field(None, gt=0, description="Point of sale ID")
    user_id: Optional[int] = Field(None, gt=0, description="User ID who made the sale")
    notes: Optional[str] = Field(None, max_length=1000, description="Sale notes")
    is_cancelled: Optional[bool] = Field(False, description="Whether the sale is cancelled")
    cancelled_at: Optional[datetime] = Field(None, description="When the sale was cancelled")
    cancelled_by_id: Optional[int] = Field(None, gt=0, description="User ID who cancelled the sale")
    is_active: Optional[bool] = Field(True, description="Whether the sale is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('At least one sale item must be provided')
        return v
    
    @field_validator('total_amount')
    def validate_total_amount(cls, v):
        if v is not None and v < 0:
            raise ValueError('Total amount must be non-negative')
        return v


class SaleCreateDTO(SaleBaseDTO):
    """
    DTO for creating a new sale.
    Inherits validation rules from SaleBaseDTO.
    """
    pass


class SaleUpdateDTO(SaleBaseDTO):
    """
    DTO for updating sale information.
    """
    pass


class SalePartialUpdateDTO(SaleBaseDTO):
    """
    DTO for partially updating sale information.
    All fields are optional.
    """
    company_id: Optional[int] = Field(None, gt=0, description="Company ID")
    items: Optional[List[SaleItemBaseDTO]] = Field(None, description="Sale items")


class SaleCancelDTO(BaseModel):
    """
    DTO for cancelling a sale.
    """
    
    cancelled_by_id: int = Field(..., gt=0, description="User ID who cancelled the sale")
    notes: Optional[str] = Field(None, max_length=1000, description="Cancellation notes")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class SaleFilterDTO(BaseModel):
    """
    DTO for filtering sales.
    """
    
    start_date: Optional[datetime] = Field(None, description="Start date for filtering")
    end_date: Optional[datetime] = Field(None, description="End date for filtering")
    point_of_sale_id: Optional[int] = Field(None, gt=0, description="Filter by point of sale ID")
    user_id: Optional[int] = Field(None, gt=0, description="Filter by user ID")
    payment_method: Optional[str] = Field(None, max_length=50, description="Filter by payment method")
    min_amount: Optional[Decimal] = Field(None, ge=0, description="Minimum total amount")
    max_amount: Optional[Decimal] = Field(None, ge=0, description="Maximum total amount")
    is_cancelled: Optional[bool] = Field(None, description="Filter by cancellation status")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('end_date')
    def validate_date_range(cls, v, info):
        start_date = info.data.get('start_date')
        if start_date and v and v < start_date:
            raise ValueError('End date must be after start date')
        return v
    
    @field_validator('max_amount')
    def validate_amount_range(cls, v, info):
        min_amount = info.data.get('min_amount')
        if min_amount is not None and v is not None and v < min_amount:
            raise ValueError('Maximum amount must be greater than or equal to minimum amount')
        return v

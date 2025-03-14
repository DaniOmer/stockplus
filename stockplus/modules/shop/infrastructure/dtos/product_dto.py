"""
Data Transfer Objects (DTOs) for the shop product application.
This module contains the DTOs for the shop product application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, StringConstraints
from typing import Optional, List
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

StripeIdStr = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=255
    )
]

CurrencyStr = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=3,
        pattern=r'^[a-z]{3}$'
    )
]

IntervalStr = Annotated[
    str,
    StringConstraints(
        pattern=r'^(day|week|month|year)$'
    )
]


class ProductBaseDTO(BaseModel):
    """
    Base DTO for shop product data.
    Contains common validation rules for shop product data.
    """
    
    # Required fields
    name: ProductNameStr = Field(..., description="Product name")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    description: Optional[str] = Field(None, max_length=2000, description="Product description")
    active: Optional[bool] = Field(True, description="Whether the product is active in Stripe")
    stripe_id: Optional[str] = Field(None, max_length=255, description="Stripe product ID")
    is_active: Optional[bool] = Field(True, description="Whether the product is active in the system")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class ProductCreateDTO(ProductBaseDTO):
    """
    DTO for creating a new shop product.
    Inherits validation rules from ProductBaseDTO.
    """
    pass


class ProductUpdateDTO(ProductBaseDTO):
    """
    DTO for updating shop product information.
    """
    pass


class ProductPartialUpdateDTO(ProductBaseDTO):
    """
    DTO for partially updating shop product information.
    All fields are optional.
    """
    name: Optional[ProductNameStr] = Field(None, description="Product name")


class ProductStripeUpdateDTO(BaseModel):
    """
    DTO for updating product Stripe information.
    """
    
    stripe_id: str = Field(..., max_length=255, description="Stripe product ID")
    active: Optional[bool] = Field(True, description="Whether the product is active in Stripe")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class PriceBaseDTO(BaseModel):
    """
    Base DTO for price data.
    Contains common validation rules for price data.
    """
    
    # Required fields
    product_id: int = Field(..., gt=0, description="Product ID this price belongs to")
    unit_amount: int = Field(..., ge=0, description="Price amount in cents")
    currency: CurrencyStr = Field("eur", description="Currency code (3-letter ISO code)")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    interval: Optional[str] = Field(None, description="Billing interval for subscriptions (day, week, month, year)")
    interval_count: Optional[int] = Field(None, gt=0, description="Number of intervals between billings")
    stripe_id: Optional[str] = Field(None, max_length=255, description="Stripe price ID")
    is_active: Optional[bool] = Field(True, description="Whether the price is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('interval')
    def validate_interval(cls, v):
        if v is not None and v not in ['day', 'week', 'month', 'year']:
            raise ValueError('Interval must be one of: day, week, month, year')
        return v
    
    @field_validator('interval_count')
    def validate_interval_count(cls, v, info):
        interval = info.data.get('interval')
        if interval and not v:
            raise ValueError('Interval count is required when interval is specified')
        if v is not None and v <= 0:
            raise ValueError('Interval count must be positive')
        return v


class PriceCreateDTO(PriceBaseDTO):
    """
    DTO for creating a new price.
    Inherits validation rules from PriceBaseDTO.
    """
    pass


class PriceUpdateDTO(PriceBaseDTO):
    """
    DTO for updating price information.
    """
    pass


class PricePartialUpdateDTO(PriceBaseDTO):
    """
    DTO for partially updating price information.
    All fields are optional.
    """
    product_id: Optional[int] = Field(None, gt=0, description="Product ID this price belongs to")
    unit_amount: Optional[int] = Field(None, ge=0, description="Price amount in cents")
    currency: Optional[CurrencyStr] = Field(None, description="Currency code (3-letter ISO code)")


class PriceStripeUpdateDTO(BaseModel):
    """
    DTO for updating price Stripe information.
    """
    
    stripe_id: str = Field(..., max_length=255, description="Stripe price ID")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }

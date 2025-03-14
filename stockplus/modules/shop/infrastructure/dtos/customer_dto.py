"""
Data Transfer Objects (DTOs) for the shop customer application.
This module contains the DTOs for the shop customer application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, StringConstraints
from typing import Optional
from typing_extensions import Annotated
from uuid import UUID


# Type annotations
StripeIdStr = Annotated[
    str,
    StringConstraints(
        min_length=3,
        max_length=255
    )
]


class CustomerBaseDTO(BaseModel):
    """
    Base DTO for customer data.
    Contains common validation rules for customer data.
    """
    
    # Required fields
    user_id: int = Field(..., gt=0, description="User ID associated with this customer")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    stripe_id: Optional[str] = Field(None, max_length=255, description="Stripe customer ID")
    is_active: Optional[bool] = Field(True, description="Whether the customer is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class CustomerCreateDTO(CustomerBaseDTO):
    """
    DTO for creating a new customer.
    Inherits validation rules from CustomerBaseDTO.
    """
    pass


class CustomerUpdateDTO(CustomerBaseDTO):
    """
    DTO for updating customer information.
    """
    pass


class CustomerPartialUpdateDTO(CustomerBaseDTO):
    """
    DTO for partially updating customer information.
    All fields are optional.
    """
    user_id: Optional[int] = Field(None, gt=0, description="User ID associated with this customer")


class CustomerStripeUpdateDTO(BaseModel):
    """
    DTO for updating customer Stripe information.
    """
    
    stripe_id: str = Field(..., max_length=255, description="Stripe customer ID")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }

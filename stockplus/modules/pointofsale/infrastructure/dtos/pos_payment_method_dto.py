"""
Data Transfer Objects (DTOs) for the pointofsale payment methods.
This module contains the DTOs for the pointofsale payment methods.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, StringConstraints
from typing import Optional
from typing_extensions import Annotated
from uuid import UUID


# Type annotations
PaymentMethodNameStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=100
    )
]


class PosPaymentMethodBaseDTO(BaseModel):
    """
    Base DTO for point of sale payment method data.
    Contains common validation rules for payment method data.
    """
    
    # Required fields
    name: PaymentMethodNameStr = Field(..., description="Payment method name")
    point_of_sale_id: int = Field(..., gt=0, description="Point of sale ID this payment method belongs to")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    description: Optional[str] = Field(None, max_length=500, description="Payment method description")
    is_active: Optional[bool] = Field(True, description="Whether the payment method is active")
    requires_confirmation: Optional[bool] = Field(False, description="Whether the payment method requires confirmation")
    confirmation_instructions: Optional[str] = Field(None, max_length=1000, description="Instructions for confirming payment")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class PosPaymentMethodCreateDTO(PosPaymentMethodBaseDTO):
    """
    DTO for creating a new point of sale payment method.
    Inherits validation rules from PosPaymentMethodBaseDTO.
    """
    pass


class PosPaymentMethodUpdateDTO(PosPaymentMethodBaseDTO):
    """
    DTO for updating point of sale payment method information.
    """
    pass


class PosPaymentMethodPartialUpdateDTO(PosPaymentMethodBaseDTO):
    """
    DTO for partially updating point of sale payment method information.
    All fields are optional.
    """
    name: Optional[PaymentMethodNameStr] = Field(None, description="Payment method name")
    point_of_sale_id: Optional[int] = Field(None, gt=0, description="Point of sale ID this payment method belongs to")


class PosPaymentMethodActivateDTO(BaseModel):
    """
    DTO for activating or deactivating a payment method.
    """
    
    is_active: bool = Field(..., description="Whether the payment method should be active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class PosPaymentMethodConfirmationDTO(BaseModel):
    """
    DTO for updating payment method confirmation settings.
    """
    
    requires_confirmation: bool = Field(..., description="Whether the payment method requires confirmation")
    confirmation_instructions: Optional[str] = Field(None, max_length=1000, description="Instructions for confirming payment")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }

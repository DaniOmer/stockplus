"""
Data Transfer Objects (DTOs) for the invoice application.
This module contains the DTOs for the invoice application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, field_validator, StringConstraints, EmailStr
from typing import Optional
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

PhoneNumberStr = Annotated[
    str,
    StringConstraints(
        pattern=r'^\+?[0-9]{8,15}$'
    )
]


class InvoiceBaseDTO(BaseModel):
    """
    Base DTO for invoice data.
    Contains common validation rules for invoice data.
    """
    
    # Required fields
    invoice_number: InvoiceNumberStr = Field(..., description="Invoice number")
    sale_id: int = Field(..., gt=0, description="Sale ID")
    company_id: int = Field(..., gt=0, description="Company ID")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    date: Optional[datetime] = Field(None, description="Invoice date")
    due_date: Optional[datetime] = Field(None, description="Due date")
    total_amount: Optional[Decimal] = Field(None, ge=0, description="Total amount")
    tax_amount: Optional[Decimal] = Field(Decimal('0.00'), ge=0, description="Tax amount")
    discount_amount: Optional[Decimal] = Field(Decimal('0.00'), ge=0, description="Discount amount")
    customer_name: Optional[str] = Field(None, max_length=100, description="Customer name")
    customer_email: Optional[EmailStr] = Field(None, description="Customer email")
    customer_phone: Optional[str] = Field(None, max_length=20, description="Customer phone")
    customer_address: Optional[str] = Field(None, max_length=255, description="Customer address")
    notes: Optional[str] = Field(None, max_length=1000, description="Invoice notes")
    is_paid: Optional[bool] = Field(False, description="Whether the invoice is paid")
    payment_date: Optional[datetime] = Field(None, description="Payment date")
    is_active: Optional[bool] = Field(True, description="Whether the invoice is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('due_date')
    def validate_due_date(cls, v, info):
        date = info.data.get('date')
        if date and v and v < date:
            raise ValueError('Due date must be after invoice date')
        return v
    
    @field_validator('payment_date')
    def validate_payment_date(cls, v, info):
        is_paid = info.data.get('is_paid')
        if is_paid and not v:
            raise ValueError('Payment date is required when invoice is marked as paid')
        return v
    
    @field_validator('total_amount', 'tax_amount', 'discount_amount')
    def validate_amounts(cls, v, info):
        field_name = info.field_name
        if v is not None and v < 0:
            raise ValueError(f'{field_name} must be non-negative')
        return v
    
    @field_validator('customer_phone')
    def validate_phone(cls, v):
        if v is not None and not v.replace('+', '').isdigit():
            raise ValueError('Phone number must contain only digits with an optional + prefix')
        return v


class InvoiceCreateDTO(InvoiceBaseDTO):
    """
    DTO for creating a new invoice.
    Inherits validation rules from InvoiceBaseDTO.
    """
    pass


class InvoiceUpdateDTO(InvoiceBaseDTO):
    """
    DTO for updating invoice information.
    """
    pass


class InvoicePartialUpdateDTO(InvoiceBaseDTO):
    """
    DTO for partially updating invoice information.
    All fields are optional.
    """
    invoice_number: Optional[InvoiceNumberStr] = Field(None, description="Invoice number")
    sale_id: Optional[int] = Field(None, gt=0, description="Sale ID")
    company_id: Optional[int] = Field(None, gt=0, description="Company ID")


class InvoicePaymentDTO(BaseModel):
    """
    DTO for recording invoice payment.
    """
    
    is_paid: bool = Field(..., description="Whether the invoice is paid")
    payment_date: Optional[datetime] = Field(None, description="Payment date")
    notes: Optional[str] = Field(None, max_length=1000, description="Payment notes")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('payment_date')
    def validate_payment_date(cls, v, info):
        is_paid = info.data.get('is_paid')
        if is_paid and not v:
            raise ValueError('Payment date is required when invoice is marked as paid')
        return v


class InvoiceFilterDTO(BaseModel):
    """
    DTO for filtering invoices.
    """
    
    start_date: Optional[datetime] = Field(None, description="Start date for filtering")
    end_date: Optional[datetime] = Field(None, description="End date for filtering")
    is_paid: Optional[bool] = Field(None, description="Filter by payment status")
    customer_name: Optional[str] = Field(None, max_length=100, description="Filter by customer name")
    customer_email: Optional[EmailStr] = Field(None, description="Filter by customer email")
    min_amount: Optional[Decimal] = Field(None, ge=0, description="Minimum total amount")
    max_amount: Optional[Decimal] = Field(None, ge=0, description="Maximum total amount")
    
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

"""
Data Transfer Objects (DTOs) for the subscription application.
This module contains the DTOs for the subscription application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, field_validator, StringConstraints
from typing import List, Optional
from typing_extensions import Annotated
from uuid import UUID
from datetime import datetime


# Type annotations
NameStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=100
    )
]

IntervalStr = Annotated[
    str,
    StringConstraints(
        pattern=r'^(day|week|month|year)$'
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

StatusStr = Annotated[
    str,
    StringConstraints(
        pattern=r'^(pending|active|cancelled|expired|trial)$'
    )
]


class FeatureBaseDTO(BaseModel):
    """
    Base DTO for subscription feature data.
    Contains common validation rules for subscription feature data.
    """
    
    # Required fields
    name: NameStr = Field(..., description="Feature name")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    description: Optional[str] = Field(None, max_length=500, description="Feature description")
    is_active: Optional[bool] = Field(True, description="Whether the feature is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class FeatureCreateDTO(FeatureBaseDTO):
    """
    DTO for creating a new subscription feature.
    Inherits validation rules from FeatureBaseDTO.
    """
    pass


class FeatureUpdateDTO(FeatureBaseDTO):
    """
    DTO for updating subscription feature information.
    """
    pass


class FeaturePartialUpdateDTO(FeatureBaseDTO):
    """
    DTO for partially updating subscription feature information.
    All fields are optional.
    """
    name: Optional[NameStr] = Field(None, description="Feature name")


class SubscriptionPlanBaseDTO(BaseModel):
    """
    Base DTO for subscription plan data.
    Contains common validation rules for subscription plan data.
    """
    
    # Required fields
    name: NameStr = Field(..., description="Plan name")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    description: Optional[str] = Field(None, max_length=500, description="Plan description")
    active: Optional[bool] = Field(True, description="Whether the plan is active in Stripe")
    feature_ids: Optional[List[int]] = Field(None, description="List of feature IDs included in this plan")
    group_id: Optional[int] = Field(None, gt=0, description="Django Group ID associated with this plan")
    permission_ids: Optional[List[int]] = Field(None, description="List of permission IDs granted by this plan")
    stripe_id: Optional[str] = Field(None, max_length=255, description="Stripe product ID")
    pos_limit: Optional[int] = Field(3, ge=0, description="Maximum number of points of sale allowed")
    is_free_trial: Optional[bool] = Field(False, description="Whether this plan offers a free trial")
    trial_days: Optional[int] = Field(30, ge=0, description="Number of days in the free trial period")
    is_active: Optional[bool] = Field(True, description="Whether the plan is active in the system")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('pos_limit')
    def validate_pos_limit(cls, v):
        if v is not None and v < 0:
            raise ValueError('Point of sale limit must be non-negative')
        return v
    
    @field_validator('trial_days')
    def validate_trial_days(cls, v, info):
        is_free_trial = info.data.get('is_free_trial')
        if is_free_trial and (v is None or v <= 0):
            raise ValueError('Trial days must be positive when free trial is enabled')
        return v


class SubscriptionPlanCreateDTO(SubscriptionPlanBaseDTO):
    """
    DTO for creating a new subscription plan.
    Inherits validation rules from SubscriptionPlanBaseDTO.
    """
    pass


class SubscriptionPlanUpdateDTO(SubscriptionPlanBaseDTO):
    """
    DTO for updating subscription plan information.
    """
    pass


class SubscriptionPlanPartialUpdateDTO(SubscriptionPlanBaseDTO):
    """
    DTO for partially updating subscription plan information.
    All fields are optional.
    """
    name: Optional[NameStr] = Field(None, description="Plan name")


class SubscriptionPricingBaseDTO(BaseModel):
    """
    Base DTO for subscription pricing data.
    Contains common validation rules for subscription pricing data.
    """
    
    # Required fields
    subscription_plan_id: int = Field(..., gt=0, description="Subscription plan ID")
    interval: IntervalStr = Field("month", description="Billing interval (day, week, month, year)")
    price: float = Field(..., ge=0, description="Price amount")
    currency: CurrencyStr = Field("eur", description="Currency code (3-letter ISO code)")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    stripe_id: Optional[str] = Field(None, max_length=255, description="Stripe price ID")
    is_active: Optional[bool] = Field(True, description="Whether the pricing is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('interval')
    def validate_interval(cls, v):
        if v not in ['day', 'week', 'month', 'year']:
            raise ValueError('Interval must be one of: day, week, month, year')
        return v
    
    @field_validator('price')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price must be non-negative')
        return v


class SubscriptionPricingCreateDTO(SubscriptionPricingBaseDTO):
    """
    DTO for creating a new subscription pricing.
    Inherits validation rules from SubscriptionPricingBaseDTO.
    """
    pass


class SubscriptionPricingUpdateDTO(SubscriptionPricingBaseDTO):
    """
    DTO for updating subscription pricing information.
    """
    pass


class SubscriptionPricingPartialUpdateDTO(SubscriptionPricingBaseDTO):
    """
    DTO for partially updating subscription pricing information.
    All fields are optional.
    """
    subscription_plan_id: Optional[int] = Field(None, gt=0, description="Subscription plan ID")
    interval: Optional[IntervalStr] = Field(None, description="Billing interval (day, week, month, year)")
    price: Optional[float] = Field(None, ge=0, description="Price amount")
    currency: Optional[CurrencyStr] = Field(None, description="Currency code (3-letter ISO code)")


class SubscriptionBaseDTO(BaseModel):
    """
    Base DTO for subscription data.
    Contains common validation rules for subscription data.
    """
    
    # Required fields
    user_id: int = Field(..., gt=0, description="User ID")
    subscription_plan_id: int = Field(..., gt=0, description="Subscription plan ID")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    company_id: Optional[int] = Field(None, gt=0, description="Company ID")
    interval: Optional[IntervalStr] = Field("month", description="Billing interval (day, week, month, year)")
    start_date: Optional[datetime] = Field(None, description="Subscription start date")
    end_date: Optional[datetime] = Field(None, description="Subscription end date")
    renewal_date: Optional[datetime] = Field(None, description="Subscription renewal date")
    status: Optional[StatusStr] = Field("pending", description="Subscription status (pending, active, cancelled, expired, trial)")
    is_active: Optional[bool] = Field(True, description="Whether the subscription is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('interval')
    def validate_interval(cls, v):
        if v is not None and v not in ['day', 'week', 'month', 'year']:
            raise ValueError('Interval must be one of: day, week, month, year')
        return v
    
    @field_validator('end_date')
    def validate_end_date(cls, v, info):
        start_date = info.data.get('start_date')
        if start_date and v and v < start_date:
            raise ValueError('End date must be after start date')
        return v
    
    @field_validator('renewal_date')
    def validate_renewal_date(cls, v, info):
        start_date = info.data.get('start_date')
        if start_date and v and v < start_date:
            raise ValueError('Renewal date must be after start date')
        return v
    
    @field_validator('status')
    def validate_status(cls, v):
        if v is not None and v not in ['pending', 'active', 'cancelled', 'expired', 'trial']:
            raise ValueError('Status must be one of: pending, active, cancelled, expired, trial')
        return v


class SubscriptionCreateDTO(SubscriptionBaseDTO):
    """
    DTO for creating a new subscription.
    Inherits validation rules from SubscriptionBaseDTO.
    """
    pass


class SubscriptionUpdateDTO(SubscriptionBaseDTO):
    """
    DTO for updating subscription information.
    """
    pass


class SubscriptionPartialUpdateDTO(SubscriptionBaseDTO):
    """
    DTO for partially updating subscription information.
    All fields are optional.
    """
    user_id: Optional[int] = Field(None, gt=0, description="User ID")
    subscription_plan_id: Optional[int] = Field(None, gt=0, description="Subscription plan ID")


class SubscriptionStatusUpdateDTO(BaseModel):
    """
    DTO for updating subscription status.
    """
    
    status: StatusStr = Field(..., description="New subscription status (pending, active, cancelled, expired, trial)")
    end_date: Optional[datetime] = Field(None, description="New end date (required for cancelled or expired status)")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('end_date')
    def validate_end_date(cls, v, info):
        status = info.data.get('status')
        if status in ['cancelled', 'expired'] and not v:
            raise ValueError('End date is required when status is cancelled or expired')
        return v

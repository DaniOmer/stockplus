from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from django.contrib.auth.models import Group, Permission


@dataclass
class Feature:
    """
    Domain model for a subscription feature.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    name: str = ""
    description: Optional[str] = None
    is_active: bool = True


@dataclass
class SubscriptionPlan:
    """
    Domain model for a subscription plan.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    name: str = ""
    description: Optional[str] = None
    active: bool = True
    features: List[Feature] = None
    group: Optional[Group] = None
    permissions: List[Permission] = None
    stripe_id: Optional[str] = None
    pos_limit: int = 3
    is_free_trial: bool = False
    trial_days: int = 30
    is_active: bool = True


@dataclass
class SubscriptionPricing:
    """
    Domain model for subscription pricing.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    subscription_plan_id: Optional[int] = None
    interval: str = "month"
    price: float = 0.0
    currency: str = "eur"
    stripe_id: Optional[str] = None
    is_active: bool = True


@dataclass
class Subscription:
    """
    Domain model for a user subscription.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    user_id: int = 0
    company_id: Optional[int] = None
    subscription_plan_id: Optional[int] = None
    interval: str = "month"
    start_date: datetime = None
    end_date: datetime = None
    renewal_date: datetime = None
    status: str = "pending"
    is_active: bool = True

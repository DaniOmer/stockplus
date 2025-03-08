from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID


@dataclass
class Product:
    """
    Domain model for a product.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    name: str = ""
    description: Optional[str] = None
    active: bool = True
    stripe_id: Optional[str] = None
    is_active: bool = True


@dataclass
class Price:
    """
    Domain model for a price.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    product_id: int = 0
    unit_amount: int = 0
    currency: str = "eur"
    interval: Optional[str] = None
    interval_count: Optional[int] = None
    stripe_id: Optional[str] = None
    is_active: bool = True

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class ProductVariant:
    """
    Domain model for a product variant.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    name: Optional[str] = None
    product_id: int = 0
    color: Optional[str] = None
    size: Optional[str] = None
    price: float = 0.0
    buy_price: Optional[float] = None
    sku: Optional[str] = None
    is_active: bool = True
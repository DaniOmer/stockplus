from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class ProductFeature:
    """
    Domain model for a product feature.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    name: str = ""
    description: Optional[str] = None
    product_id: int = 0
    is_active: bool = True
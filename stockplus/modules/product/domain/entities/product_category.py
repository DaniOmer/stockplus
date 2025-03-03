from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class ProductCategory:
    """
    Domain model for a product category.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    name: str = ""
    description: Optional[str] = None
    parent_id: Optional[int] = None
    company_id: int = 0
    is_active: bool = True
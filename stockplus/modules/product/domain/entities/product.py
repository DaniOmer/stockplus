from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID

from stockplus.modules.product.domain.entities.product_feature import ProductFeature
from stockplus.modules.product.domain.entities.product_variant import ProductVariant


@dataclass
class Product:
    """
    Domain model for a product.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    name: str = ""
    description: Optional[str] = None
    brand_id: Optional[int] = None
    category_id: Optional[int] = None
    company_id: int = 0
    features: List[ProductFeature] = field(default_factory=list)
    variants: List[ProductVariant] = field(default_factory=list)
    is_active: bool = True
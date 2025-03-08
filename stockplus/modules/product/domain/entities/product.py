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
    barcode: Optional[str] = None
    barcode_image: Optional[str] = None
    stock: int = 0
    low_stock_threshold: int = 5
    brand_id: Optional[int] = None
    category_id: Optional[int] = None
    company_id: int = 0
    features: List[ProductFeature] = field(default_factory=list)
    variants: List[ProductVariant] = field(default_factory=list)
    is_active: bool = True
    
    @property
    def is_low_stock(self) -> bool:
        """
        Check if the product has low stock.
        
        Returns:
            True if the stock is less than or equal to the low stock threshold, False otherwise.
        """
        return self.stock <= self.low_stock_threshold

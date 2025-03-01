from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID


@dataclass
class Brand:
    """
    Domain model for a brand.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    name: str = ""
    description: Optional[str] = None
    logo_url: Optional[str] = None
    company_id: int = 0
    is_active: bool = True


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


@dataclass
class PointOfSaleProductVariant:
    """
    Domain model for a point of sale product variant.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    point_of_sale_id: int = 0
    product_variant_id: int = 0
    stock: int = 0
    price: Optional[float] = None
    is_active: bool = True

"""
Models package.
This package contains the domain models.
"""
from stockplus.modules.pointofsale.domain.models import PointOfSale
from stockplus.modules.product.domain.models import Product

__all__ = [
    'PointOfSale',
    'Product'
]
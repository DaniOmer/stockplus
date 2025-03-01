"""
ORM package.
This package contains the ORM models for the infrastructure layer.
"""

from django.conf import settings

if 'stockplus.modules.pointofsale' in settings.INSTALLED_APPS:
    from stockplus.modules.pointofsale.infrastructure.orm import PointOfSale

if 'stockplus.modules.product' in settings.INSTALLED_APPS:
    from stockplus.modules.product.infrastructure.orm import (
        Brand, ProductCategory, Product, ProductFeature, 
        ProductVariant, PointOfSaleProductVariant
    )
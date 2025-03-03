"""
ORM package.
This package contains the ORM models for the infrastructure layer.
"""

from django.conf import settings

if 'stockplus.modules.pointofsale' in settings.INSTALLED_APPS:
    from stockplus.modules.pointofsale.infrastructure import models as pointofsale_models
    class PointOfSale(pointofsale_models.PointOfSale): pass
    class PosPaymentMethod(pointofsale_models.PosPaymentMethod): pass

if 'stockplus.modules.product' in settings.INSTALLED_APPS:
    from stockplus.modules.product.infrastructure import models as product_models
    class Brand(product_models.Brand): pass
    class ProductCategory(product_models.ProductCategory): pass
    class Product(product_models.Product): pass
    class ProductFeature(product_models.ProductFeature): pass
    class ProductVariant(product_models.ProductVariant): pass
    
from django.conf import settings

if 'stockplus.applications.pointofsale' in settings.INSTALLED_APPS:
    from stockplus.applications.pointofsale import models as models_pointofsale
    class PointOfSale(models_pointofsale.PointOfSale): pass

if 'stockplus.applications.product' in settings.INSTALLED_APPS:
    from stockplus.applications.product import models as models_product
    class Brand(models_product.Brand): pass
    class ProductCategory(models_product.ProductCategory): pass
    class Product(models_product.Product): pass
    class ProductFeature(models_product.ProductFeature): pass
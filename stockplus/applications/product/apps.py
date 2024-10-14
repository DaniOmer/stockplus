from django.apps import AppConfig

class Config:
    class ForeignKey:
        company = 'builder.Company'
        point_of_sale = 'stockplus.PointOfSale'
        brand = 'stockplus.Brand'
        product_category = 'stockplus.ProductCategory'
        product = 'stockplus.Product'
        product_variant = 'stockplus.ProductVariant'

class ProductConfig(AppConfig, Config):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stockplus.applications.product'

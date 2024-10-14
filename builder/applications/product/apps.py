from django.apps import AppConfig

class Config:
    class ForeignKey:
        brand = 'builder.Brand'
        product_category = 'builder.ProductCategory'
        product = 'builder.Product'

class ProductConfig(AppConfig, Config):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'builder.applications.product'

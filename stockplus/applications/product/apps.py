from django.apps import AppConfig

class Config:
    class ForeignKey:
        company = 'builder.Company'
        brand = 'stockplus.Brand'
        product_category = 'stockplus.ProductCategory'
        product = 'stockplus.Product'

class ProductConfig(AppConfig, Config):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stockplus.applications.product'

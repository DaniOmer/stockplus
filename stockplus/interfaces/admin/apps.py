from django.apps import AppConfig
from django.contrib import admin


class AdminInterfaceConfig(AppConfig):
    name = 'stockplus.interfaces.admin'
    label = 'stockplus_admin'
    verbose_name = 'Stockplus Admin Interface'

    def ready(self):
        from django.contrib import admin
        
        # Import Point of Sale models and admin classes
        from stockplus.infrastructure.models import PointOfSale
        from stockplus.modules.pointofsale.interfaces.admin import PointOfSaleAdmin
        
        # Import Product models and admin classes
        # from stockplus.infrastructure.models import (
        #     BrandORM, ProductCategoryORM, ProductORM, 
        #     ProductFeatureORM, ProductVariantORM, PointOfSaleProductVariantORM
        # )
        # from stockplus.modules.product.interfaces.admin import (
        #     BrandAdmin, ProductCategoryAdmin, ProductAdmin,
        #     ProductFeatureAdmin, ProductVariantAdmin, PointOfSaleProductVariantAdmin
        # )
        
        # Register Point of Sale models
        admin.site.register(PointOfSale, PointOfSaleAdmin)
        
        # Register Product models
        # admin.site.register(BrandORM, BrandAdmin)
        # admin.site.register(ProductCategoryORM, ProductCategoryAdmin)
        # admin.site.register(ProductORM, ProductAdmin)
        # admin.site.register(ProductFeatureORM, ProductFeatureAdmin)
        # admin.site.register(ProductVariantORM, ProductVariantAdmin)
        # admin.site.register(PointOfSaleProductVariantORM, PointOfSaleProductVariantAdmin)

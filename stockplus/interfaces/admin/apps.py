from django.apps import AppConfig
from django.contrib import admin


class AdminInterfaceConfig(AppConfig):
    name = 'stockplus.interfaces.admin'
    label = 'stockplus_admin'  # Utiliser un label unique pour éviter les conflits
    verbose_name = 'Stockplus Admin Interface'

    def ready(self):
        # Register admin models here to avoid circular imports
        from django.contrib import admin
        
        # Import Point of Sale models and admin classes
        from stockplus.modules.pointofsale.infrastructure.orm.orm import PointOfSaleORM
        from stockplus.modules.pointofsale.interfaces.admin import PointOfSaleAdmin
        
        # Import Product models and admin classes
        from stockplus.modules.product.infrastructure.orm.orm import (
            BrandORM, ProductCategoryORM, ProductORM, 
            ProductFeatureORM, ProductVariantORM, PointOfSaleProductVariantORM
        )
        from stockplus.modules.product.interfaces.admin import (
            BrandAdmin, ProductCategoryAdmin, ProductAdmin,
            ProductFeatureAdmin, ProductVariantAdmin, PointOfSaleProductVariantAdmin
        )
        
        # Register Point of Sale models
        admin.site.register(PointOfSaleORM, PointOfSaleAdmin)
        
        # Register Product models
        admin.site.register(BrandORM, BrandAdmin)
        admin.site.register(ProductCategoryORM, ProductCategoryAdmin)
        admin.site.register(ProductORM, ProductAdmin)
        admin.site.register(ProductFeatureORM, ProductFeatureAdmin)
        admin.site.register(ProductVariantORM, ProductVariantAdmin)
        admin.site.register(PointOfSaleProductVariantORM, PointOfSaleProductVariantAdmin)

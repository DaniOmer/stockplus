from django.contrib import admin

from stockplus.modules.product.infrastructure.orm.orm import (
    BrandORM, ProductCategoryORM, ProductORM, 
    ProductFeatureORM, ProductVariantORM, PointOfSaleProductVariantORM
)

class BrandAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'logo_url', 'company']
    search_fields = ['name']

class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'parent', 'company']
    search_fields = ['name']

class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'brand', 'category', 'company']
    search_fields = ['name']

class ProductFeatureAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'product']
    search_fields = ['name']

class ProductVariantAdmin(admin.ModelAdmin):
    fields = ['name', 'product', 'color', 'size', 'price', 'buy_price', 'sku']
    search_fields = ['name', 'sku']

class PointOfSaleProductVariantAdmin(admin.ModelAdmin):
    fields = ['point_of_sale', 'product_variant', 'stock', 'price']
    search_fields = ['point_of_sale__name', 'product_variant__name']

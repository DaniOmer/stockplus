from django.contrib import admin

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

from stockplus.modules.product.infrastructure.orm.orm import (
    BrandORM, ProductCategoryORM, ProductORM, 
    ProductFeatureORM, ProductVariantORM, PointOfSaleProductVariantORM
)

# Aliases for backward compatibility
Brand = BrandORM
ProductCategory = ProductCategoryORM
Product = ProductORM
ProductFeature = ProductFeatureORM
ProductVariant = ProductVariantORM
PointOfSaleProductVariant = PointOfSaleProductVariantORM

__all__ = [
    'BrandORM', 'ProductCategoryORM', 'ProductORM', 
    'ProductFeatureORM', 'ProductVariantORM', 'PointOfSaleProductVariantORM',
    'Brand', 'ProductCategory', 'Product',
    'ProductFeature', 'ProductVariant', 'PointOfSaleProductVariant'
]

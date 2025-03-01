from django.db import models

from builder.models import Company
from builder.models.base import Base
from stockplus.modules.pointofsale.infrastructure.orm.orm import PointOfSaleORM


class BrandORM(Base):
    """
    ORM model for a brand.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    company = models.ForeignKey(Company, related_name="brands", on_delete=models.CASCADE)

    class Meta:
        db_table = 'stockplus_brand'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return str(self.name)


class ProductCategoryORM(Base):
    """
    ORM model for a product category.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, related_name="product_categories", on_delete=models.CASCADE)

    class Meta:
        db_table = 'stockplus_productcategory'
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
    
    def __str__(self):
        return str(self.name)


class ProductORM(Base):
    """
    ORM model for a product.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    brand = models.ForeignKey(BrandORM, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(ProductCategoryORM, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, related_name="products", on_delete=models.CASCADE)

    class Meta:
        db_table = 'stockplus_product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return str(self.name)


class ProductFeatureORM(Base):
    """
    ORM model for a product feature.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(ProductORM, related_name="features", on_delete=models.CASCADE)

    class Meta:
        db_table = 'stockplus_productfeature'
        verbose_name = 'Product Feature'
        verbose_name_plural = 'Product Features'
    
    def __str__(self):
        return str(self.name)
    

class ProductVariantORM(Base):
    """
    ORM model for a product variant.
    """
    name = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(ProductORM, related_name="variants", on_delete=models.CASCADE)
    color = models.CharField(max_length=20, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        db_table = 'stockplus_productvariant'
        verbose_name = 'Product Variant'
        verbose_name_plural = 'Product Variants'
        unique_together = ('product', 'color', 'size')

    def __str__(self):
        return f"{self.product.name} - {self.color} {self.size}"


class PointOfSaleProductVariantORM(Base):
    """
    ORM model for a point of sale product variant.
    """
    point_of_sale = models.ForeignKey(PointOfSaleORM, related_name="product_variants", on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariantORM, related_name="point_of_sale_variants", on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'stockplus_pointofsaleproductvariant'
        verbose_name = 'Point of Sale Product Variant'
        verbose_name_plural = 'Point of Sale Product Variants'
        unique_together = ('point_of_sale', 'product_variant')

    def __str__(self):
        return f"{self.point_of_sale.name} - {self.product_variant} (Stock: {self.stock})"

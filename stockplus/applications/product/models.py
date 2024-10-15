from django.db import models

from builder.models.base import Base
from stockplus.applications.product.apps import ProductConfig as conf

class Brand(Base):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    company = models.ForeignKey(conf.ForeignKey.company, related_name="brands", on_delete=models.CASCADE)

    class Meta():
        abstract = True

    def __str__(self):
        return str(self.name)

class ProductCategory(Base):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(conf.ForeignKey.company, related_name="product_categories", on_delete=models.CASCADE)

    class Meta():
        abstract = True
    
    def __str__(self):
        return str(self.name)

class Product(Base):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    brand = models.ForeignKey(conf.ForeignKey.brand, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(conf.ForeignKey.product_category, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(conf.ForeignKey.company, related_name="products", on_delete=models.CASCADE)

    class Meta():
        abstract = True
    
    def __str__(self):
        return str(self.name)

class ProductFeature(Base):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(conf.ForeignKey.product, related_name="features", on_delete=models.CASCADE)

    class Meta():
        abstract = True
    
    def __str__(self):
        return str(self.name)
    
class ProductVariant(Base):
    name = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(conf.ForeignKey.product, related_name="variants", on_delete=models.CASCADE)
    color = models.CharField(max_length=20, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=120, null=True, blank=True)

    class Meta():
        abstract = True
        unique_together = ('product', 'color', 'size')

    def __str__(self):
        return f"{self.product.name} - {self.color} {self.size}"

class PointOfSaleProductVariant(Base):
    point_of_sale = models.ForeignKey(conf.ForeignKey.point_of_sale, related_name="product_variants", on_delete=models.CASCADE)
    product_variant = models.ForeignKey(conf.ForeignKey.product_variant, related_name="point_of_sale_variants", on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        abstract = True
        unique_together = ('point_of_sale', 'product_variant')

    def __str__(self):
        return f"{self.point_of_sale.name} - {self.product_variant} (Stock: {self.stock})"
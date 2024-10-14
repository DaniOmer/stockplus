from django.db import models

from builder.models.base import Base
from builder.applications.product.apps import ProductConfig as conf


class Brand(Base):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)

    class Meta():
        abstract = True


class ProductCategory(Base):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)

    class Meta():
        abstract = True

class Product(Base):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    brand = models.ForeignKey(conf.ForeignKey.brand, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(conf.ForeignKey.product_category, related_name="products", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta():
        abstract = True

class ProductFeature(Base):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(conf.ForeignKey.product, related_name="products", on_delete=models.CASCADE)
    
    class Meta():
        abstract = True
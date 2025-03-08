import logging
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from stockplus.models.base import Base

logger = logging.getLogger(__name__)

User = get_user_model()


class Customer(Base):
    """
    ORM model for a customer.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop_customer')
    stripe_id = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        db_table = 'stockplus_shop_customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return f"Customer for {self.user}"


class Product(Base):
    """
    ORM model for a product.
    PRODUCT is equivalent to STRIPE PRODUCT
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    
    class Meta:
        db_table = 'stockplus_shop_product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return f"{self.name}"


class Price(Base):
    """
    ORM model for a price.
    PRICE is equivalent to STRIPE PRICE
    """
    product = models.ForeignKey(Product, related_name='prices', on_delete=models.CASCADE)
    unit_amount = models.IntegerField()  # Amount in cents
    currency = models.CharField(max_length=10, default='eur')
    interval = models.CharField(max_length=100, blank=True, null=True)
    interval_count = models.IntegerField(blank=True, null=True)
    stripe_id = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        db_table = 'stockplus_price'
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'
    
    def __str__(self):
        return f"{self.product.name} - {self.unit_amount/100} {self.currency}"

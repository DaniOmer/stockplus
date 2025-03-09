import logging
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from stockplus.models.base import Base
from stockplus.modules.shop.services import CustomerService

logger = logging.getLogger(__name__)

User = get_user_model()


class Customer(Base):
    """
    ORM model for a customer.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop_customer')
    stripe_id = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        db_table = 'stockplus_stripecustomer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return f"Customer for {self.user}"

    def get_stripe_id(self):
        if self.user.is_verified:
            try:
                stripe_id = CustomerService.create_stripe_customer(
                    name=self.user.fullname,
                    email=self.user.email,
                    metadata={'user_id': self.user.id}
                )
                return stripe_id
            except Exception as e:
                logger.info(f"Failed to create stripe Customer for user {self.user.fullname} : {e}")
                return None
        return None


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
        db_table = 'stockplus_stripeproduct'
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
    unit_amount = models.IntegerField()
    currency = models.CharField(max_length=10, default='eur')
    interval = models.CharField(max_length=100, blank=True, null=True)
    interval_count = models.IntegerField(blank=True, null=True)
    stripe_id = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        db_table = 'stockplus_stripeprice'
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'
    
    def __str__(self):
        return f"{self.product.name} - {self.unit_amount/100} {self.currency}"

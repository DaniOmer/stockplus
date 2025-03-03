from django.db import models
from django.utils.translation import gettext_lazy as _

from builder.models.base import Base

class Product(Base):
    """
    ORM model for a product.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    brand = brand = models.ForeignKey(
        'stockplus.Brand',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='brand_products',
        help_text=_('The brand this product belongs to.'),
    )
    category = models.ForeignKey(
        'stockplus.ProductCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category_products',
        help_text=_('The category this product belongs to.'),
    )
    company = models.ForeignKey(
        'builder.Company',
        on_delete=models.CASCADE,
        related_name='company_products',
        help_text=_('The company this product belongs to.'),
    )
    point_of_sale = models.ForeignKey(
        'stockplus.PointOfSale',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pos_products',
        help_text=_('The point of sale this product belongs to.'),
    )

    class Meta:
        db_table = 'stockplus_product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        abstract = True
    
    def __str__(self):
        return str(self.name)
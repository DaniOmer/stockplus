from django.db import models
from django.utils.translation import gettext_lazy as _

from builder.models.base import Base
    

class ProductVariant(Base):
    """
    ORM model for a product variant.
    """
    name = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(
        'stockplus.Product',
        on_delete=models.CASCADE,
        related_name='product_variants',
        help_text=_('The product this variant belongs to.'),
    )
    color = models.CharField(max_length=20, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        db_table = 'stockplus_product_variant'
        verbose_name = 'Product Variant'
        verbose_name_plural = 'Product Variants'
        unique_together = ('product', 'color', 'size')
        abstract = True

    def __str__(self):
        return f"{self.product.name} - {self.color} {self.size}"
from django.db import models
from django.utils.translation import gettext_lazy as _

from stockplus.models.base import Base
from stockplus.modules.product.infrastructure.models import Product, ProductVariant
from stockplus.modules.sales.infrastructure.models.sale_model import Sale


class SaleItem(Base):
    """
    ORM model for a sale item.
    """
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='sale_items',
        help_text=_('The sale this item belongs to.'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='product_sales',
        help_text=_('The product that was sold.'),
    )
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='variant_sales',
        help_text=_('The product variant that was sold.'),
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'stockplus_sale_item'
        verbose_name = 'Sale Item'
        verbose_name_plural = 'Sale Items'
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def save(self, *args, **kwargs):
        """
        Override the save method to calculate the total price.
        """
        self.total_price = (self.unit_price * self.quantity) - self.discount
        super().save(*args, **kwargs)

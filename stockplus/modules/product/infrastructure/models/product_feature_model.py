from django.db import models
from django.utils.translation import gettext_lazy as _

from stockplus.models.base import Base
from stockplus.modules.product.infrastructure.models import Product

class ProductFeature(Base):
    """
    ORM model for a product feature.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_features',
        help_text=_('The product this feature belongs to.'),
    )

    class Meta:
        db_table = 'stockplus_product_feature'
        verbose_name = 'Product Feature'
        verbose_name_plural = 'Product Features'
    
    def __str__(self):
        return str(self.name)

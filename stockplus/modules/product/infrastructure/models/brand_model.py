from django.db import models
from django.utils.translation import gettext_lazy as _

from builder.models.base import Base

class Brand(Base):
    """
    ORM model for a brand.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    company = models.ForeignKey(
        'builder.Company',
        on_delete=models.CASCADE,
        related_name='company_brands',
        help_text=_('The company this brand belongs to.'),
    )

    class Meta:
        db_table = 'stockplus_brand'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        abstract = True

    def __str__(self):
        return str(self.name)
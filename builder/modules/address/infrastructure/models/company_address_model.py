"""
Models for the address application.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from builder.models.base import Base
from builder.modules.address.infrastructure.models.base_address import Address as BaseAddress

class CompanyAddress(BaseAddress):
    """
    Company address model.
    """
    company = models.ForeignKey(
        'builder.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='company_addresses',
        help_text=_('The company this address belongs to.'),
    )

    class Meta(Base.Meta):
        abstract = True
        verbose_name = "company address"
        verbose_name_plural = "company addresses"

"""
Models for the address application.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from stockplus.modules.address.infrastructure.models.base_address import Address as BaseAddress
from stockplus.modules.company.infrastructure.models import Company as CompanyORM

class CompanyAddress(BaseAddress):
    """
    Company address model.
    """
    company = models.ForeignKey(
        CompanyORM,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='company_addresses',
        help_text=_('The company this address belongs to.'),
    )

    class Meta:
        db_table = 'stockplus_companyaddress'
        verbose_name = "company address"
        verbose_name_plural = "company addresses"

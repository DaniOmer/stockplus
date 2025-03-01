"""
Models for the address application.
"""
from django.db import models
from django.conf import settings

from builder.modules.address.domain.models.address import Address
from builder.modules.address.domain.models.address import Address as BaseAddress


class UserAddress(BaseAddress):
    """
    User address model.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_addresses')

    class Meta(BaseAddress.Meta):
        abstract = False
        verbose_name = "user address"
        verbose_name_plural = "user addresses"


class CompanyAddress(BaseAddress):
    """
    Company address model.
    """
    company = models.ForeignKey('builder.Company', on_delete=models.CASCADE, related_name='addresses')

    class Meta(BaseAddress.Meta):
        abstract = False
        verbose_name = "company address"
        verbose_name_plural = "company addresses"

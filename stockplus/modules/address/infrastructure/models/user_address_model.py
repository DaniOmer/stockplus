"""
Models for the address application.
"""
from django.db import models
from django.conf import settings

from stockplus.modules.address.infrastructure.models.base_address import Address as BaseAddress

class UserAddress(BaseAddress):
    """
    User address model.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_addresses')

    class Meta:
        db_table = 'stockplus_useraddress'
        verbose_name = "user address"
        verbose_name_plural = "user addresses"


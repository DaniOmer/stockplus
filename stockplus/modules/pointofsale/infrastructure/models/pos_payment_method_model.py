from django.db import models

from stockplus.models.base import Base
from stockplus.modules.pointofsale.infrastructure.models import PointOfSale

class PosPaymentMethod(Base):
    """
    ORM model for a payment method.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    point_of_sale = models.ForeignKey(PointOfSale, on_delete=models.CASCADE, related_name='pos_payment_methods')
    is_active = models.BooleanField(default=True)
    requires_confirmation = models.BooleanField(default=False)
    confirmation_instructions = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'stockplus_pospaymentmethod'
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'

    def __str__(self):
        return self.name

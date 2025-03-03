from django.db import models

from builder.models.base import Base

class PosPaymentMethod(Base):
    """
    ORM model for a payment method.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    point_of_sale = models.ForeignKey('stockplus.PointOfSale', on_delete=models.CASCADE, related_name='pos_payment_methods')
    is_active = models.BooleanField(default=True)
    requires_confirmation = models.BooleanField(default=False)
    confirmation_instructions = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'stockplus_paymentmethod'
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'
        abstract = True

    def __str__(self):
        return self.name

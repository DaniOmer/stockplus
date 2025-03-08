from django.db import models
from django.utils.translation import gettext_lazy as _

from stockplus.models.base import Base
from stockplus.modules.company.infrastructure.models import Company
from stockplus.modules.pointofsale.infrastructure.models import PointOfSale
from stockplus.modules.user.infrastructure.models import User


class Sale(Base):
    """
    ORM model for a sale.
    """
    PAYMENT_METHODS = [
        ('cash', _('Cash')),
        ('card', _('Card')),
        ('transfer', _('Bank Transfer')),
        ('check', _('Check')),
        ('mobile', _('Mobile Payment')),
        ('other', _('Other')),
    ]
    
    invoice_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    point_of_sale = models.ForeignKey(
        PointOfSale,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pos_sales',
        help_text=_('The point of sale where this sale was made.'),
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='company_sales',
        help_text=_('The company this sale belongs to.'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_sales',
        help_text=_('The user who made this sale.'),
    )
    is_cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancelled_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cancelled_sales',
        help_text=_('The user who cancelled this sale.'),
    )
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'stockplus_sale'
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
        ordering = ['-date']
    
    def __str__(self):
        return f"Sale {self.invoice_number or self.id} - {self.date.strftime('%Y-%m-%d')}"
    
    @property
    def item_count(self):
        """
        Get the total number of items in the sale.
        
        Returns:
            The total number of items.
        """
        return sum(item.quantity for item in self.sale_items.all())

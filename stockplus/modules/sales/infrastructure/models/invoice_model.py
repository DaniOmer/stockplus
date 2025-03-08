from django.db import models
from django.utils.translation import gettext_lazy as _

from stockplus.models.base import Base
from stockplus.modules.company.infrastructure.models import Company
from stockplus.modules.sales.infrastructure.models.sale_model import Sale


class Invoice(Base):
    """
    ORM model for an invoice.
    """
    invoice_number = models.CharField(max_length=50, unique=True)
    sale = models.OneToOneField(
        Sale,
        on_delete=models.CASCADE,
        related_name='invoice',
        help_text=_('The sale this invoice is for.'),
    )
    date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='company_invoices',
        help_text=_('The company this invoice belongs to.'),
    )
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone = models.CharField(max_length=20, null=True, blank=True)
    customer_address = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'stockplus_invoice'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ['-date']
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.date.strftime('%Y-%m-%d')}"
    
    @property
    def net_amount(self):
        """
        Calculate the net amount (total - discount).
        
        Returns:
            The net amount.
        """
        return self.total_amount - self.discount_amount
    
    @property
    def grand_total(self):
        """
        Calculate the grand total (net + tax).
        
        Returns:
            The grand total.
        """
        return self.net_amount + self.tax_amount

from django.db import models
from django.utils.translation import gettext_lazy as _

from stockplus.models.base import Base
from stockplus.modules.company.infrastructure.models import Company as CompanyORM
from stockplus.modules.user.infrastructure.models.user_model import User

class PointOfSale(Base):
    """
    ORM model for a point of sale.
    """
    TYPE_CHOICES = [
        ('store', 'Physical Store'),
        ('warehouse', 'Warehouse'),
        ('online', 'Online Store'),
    ]
    
    name = models.CharField(max_length=255)
    company = models.ForeignKey(
        CompanyORM,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='company_pos',
        help_text=_('The company this point of sale belongs to.'),
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='store')
    collaborators = models.ManyToManyField(User, related_name='assigned_point_of_sales')
    opening_hours = models.CharField(max_length=255, blank=True, null=True)
    closing_hours = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'stockplus_pointofsale'
        verbose_name = 'Point of Sale'
        verbose_name_plural = 'Points of Sale'

    def __str__(self):
        return self.name

from django.db import models

from builder.models import Company, User
from builder.models.base import Base


class PointOfSaleORM(Base):
    """
    ORM model for a point of sale.
    """
    TYPE_CHOICES = [
        ('store', 'Physical Store'),
        ('warehouse', 'Warehouse'),
        ('online', 'Online Store'),
    ]
    
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='point_of_sale')
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

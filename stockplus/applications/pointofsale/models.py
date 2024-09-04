from django.db import models

from builder.models import Company, User
from builder.models.base import Base


TYPE_CHOICES = [
        ('store', 'Physical Store'),
        ('warehouse', 'Warehouse'),
        ('online', 'Online Store'),
    ]

class PointOfSale(Base):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='point_of_sale')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='store')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_point_of_sale')
    opening_hours = models.CharField(max_length=255, blank=True, null=True)
    closing_hours = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

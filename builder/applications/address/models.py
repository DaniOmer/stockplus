from django.db import models

from builder.models.base import Base

class Address(Base):
    address = models.CharField(max_length=255, blank=True, null=True)
    complement = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    state_code = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255, blank=True, null=True)
    cedex = models.CharField(max_length=255, null=True, blank=True)
    cedex_code = models.CharField(max_length=255, null=True, blank=True)
    special = models.CharField(max_length=255, null=True, blank=True)
    index = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return f"{self.address}, {self.city}, {self.postal_code}, {self.country}"
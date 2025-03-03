"""
Domain entities for the address application.
This module contains django base model for the address.
"""
from django.db import models

from builder.models.base import Base

class Address(Base):
    """
    Base model for address entities.
    """
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
    
    def get_full_address(self):
        """
        Get the full address as a string.
        
        Returns:
            str: The full address
        """
        parts = []
        
        if self.address:
            parts.append(self.address)
        
        if self.complement:
            parts.append(self.complement)
        
        city_parts = []
        if self.postal_code:
            city_parts.append(self.postal_code)
        
        if self.city:
            city_parts.append(self.city)
        
        if city_parts:
            parts.append(" ".join(city_parts))
        
        if self.state:
            parts.append(self.state)
        
        if self.country:
            parts.append(self.country)
        
        return ", ".join(parts)
    
    def get_coordinates(self):
        """
        Get the coordinates as a tuple.
        
        Returns:
            tuple: The latitude and longitude
        """
        if self.latitude is not None and self.longitude is not None:
            return (float(self.latitude), float(self.longitude))
        return None

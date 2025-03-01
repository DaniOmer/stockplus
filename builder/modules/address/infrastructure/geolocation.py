"""
Geolocation services for the address application.
"""
import logging
from typing import Dict, Any, Tuple, Optional
import requests

from builder.modules.address.application.interfaces import GeolocationServiceInterface
from builder.modules.address.domain.exceptions import GeolocationException

logger = logging.getLogger(__name__)


class GoogleMapsGeolocationService(GeolocationServiceInterface):
    """Geolocation service using Google Maps API."""
    
    def __init__(self, api_key: str):
        """
        Initialize the service with an API key.
        
        Args:
            api_key: The Google Maps API key
        """
        self.api_key = api_key
        self.geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    def geocode_address(self, address: Any) -> Tuple[float, float]:
        """
        Convert an address to coordinates.
        
        Args:
            address: The address to geocode
            
        Returns:
            Tuple[float, float]: The latitude and longitude
            
        Raises:
            GeolocationException: If the address cannot be geocoded
        """
        try:
            # Build the address string
            address_str = self._build_address_string(address)
            
            # Make the API request
            params = {
                'address': address_str,
                'key': self.api_key
            }
            
            response = requests.get(self.geocode_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'OK':
                raise GeolocationException(f"Geocoding failed: {data['status']}")
            
            if not data['results']:
                raise GeolocationException("No results found")
            
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        except Exception as e:
            logger.error(f"Failed to geocode address: {str(e)}")
            raise GeolocationException(f"Failed to geocode address: {str(e)}")
    
    def reverse_geocode(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Convert coordinates to an address.
        
        Args:
            latitude: The latitude
            longitude: The longitude
            
        Returns:
            Dict[str, Any]: The address data
            
        Raises:
            GeolocationException: If the coordinates cannot be reverse geocoded
        """
        try:
            # Make the API request
            params = {
                'latlng': f"{latitude},{longitude}",
                'key': self.api_key
            }
            
            response = requests.get(self.geocode_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'OK':
                raise GeolocationException(f"Reverse geocoding failed: {data['status']}")
            
            if not data['results']:
                raise GeolocationException("No results found")
            
            result = data['results'][0]
            
            # Extract address components
            address_data = {}
            
            for component in result['address_components']:
                types = component['types']
                
                if 'street_number' in types:
                    address_data['street_number'] = component['long_name']
                elif 'route' in types:
                    address_data['route'] = component['long_name']
                elif 'locality' in types:
                    address_data['city'] = component['long_name']
                elif 'postal_code' in types:
                    address_data['postal_code'] = component['long_name']
                elif 'administrative_area_level_1' in types:
                    address_data['state'] = component['long_name']
                    address_data['state_code'] = component['short_name']
                elif 'country' in types:
                    address_data['country'] = component['long_name']
                    address_data['country_code'] = component['short_name']
            
            # Build the address string
            address_parts = []
            if 'street_number' in address_data:
                address_parts.append(address_data['street_number'])
            if 'route' in address_data:
                address_parts.append(address_data['route'])
            
            address_data['address'] = ' '.join(address_parts) if address_parts else result['formatted_address']
            
            return address_data
        except Exception as e:
            logger.error(f"Failed to reverse geocode coordinates: {str(e)}")
            raise GeolocationException(f"Failed to reverse geocode coordinates: {str(e)}")
    
    def _build_address_string(self, address: Any) -> str:
        """
        Build an address string from an address object.
        
        Args:
            address: The address object
            
        Returns:
            str: The address string
        """
        parts = []
        
        # Add the street address
        if hasattr(address, 'address') and address.address:
            parts.append(address.address)
        
        # Add the city and postal code
        city_parts = []
        if hasattr(address, 'postal_code') and address.postal_code:
            city_parts.append(address.postal_code)
        
        if hasattr(address, 'city') and address.city:
            city_parts.append(address.city)
        
        if city_parts:
            parts.append(' '.join(city_parts))
        
        # Add the state
        if hasattr(address, 'state') and address.state:
            parts.append(address.state)
        
        # Add the country
        if hasattr(address, 'country') and address.country:
            parts.append(address.country)
        
        return ', '.join(parts)


class DummyGeolocationService(GeolocationServiceInterface):
    """Dummy geolocation service for testing."""
    
    def geocode_address(self, address: Any) -> Tuple[float, float]:
        """
        Convert an address to coordinates.
        
        Args:
            address: The address to geocode
            
        Returns:
            Tuple[float, float]: The latitude and longitude
        """
        # Return dummy coordinates
        return 0.0, 0.0
    
    def reverse_geocode(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Convert coordinates to an address.
        
        Args:
            latitude: The latitude
            longitude: The longitude
            
        Returns:
            Dict[str, Any]: The address data
        """
        # Return dummy address data
        return {
            'address': '123 Main St',
            'city': 'Anytown',
            'postal_code': '12345',
            'state': 'State',
            'state_code': 'ST',
            'country': 'Country',
            'country_code': 'CO'
        }


def get_geolocation_service() -> Optional[GeolocationServiceInterface]:
    """
    Get the configured geolocation service.
    
    Returns:
        Optional[GeolocationServiceInterface]: The geolocation service, or None if not configured
    """
    from django.conf import settings
    
    if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
        return GoogleMapsGeolocationService(settings.GOOGLE_MAPS_API_KEY)
    
    if hasattr(settings, 'USE_DUMMY_GEOLOCATION') and settings.USE_DUMMY_GEOLOCATION:
        return DummyGeolocationService()
    
    return None

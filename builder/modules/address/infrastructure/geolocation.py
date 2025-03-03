"""
Geolocation service for the address application.
This module contains the geolocation service for the address application.
"""

import logging
from typing import Dict, Tuple, Optional

from django.conf import settings

from builder.modules.address.application.interfaces import GeolocationServiceInterface
from builder.modules.address.domain.exceptions import (
    GeolocationServiceUnavailableException,
    InvalidCoordinatesException
)

logger = logging.getLogger(__name__)


class GoogleMapsGeolocationService(GeolocationServiceInterface):
    """
    Google Maps geolocation service implementation.

    This class implements the GeolocationServiceInterface using the Google Maps API.
    """

    def __init__(self, api_key=None):
        """
        Initialize a new GoogleMapsGeolocationService instance.

        Args:
            api_key: The Google Maps API key (optional, defaults to settings.GOOGLE_MAPS_API_KEY)
        """
        self.api_key = api_key or getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
        if not self.api_key:
            logger.warning("Google Maps API key not provided. Geocoding will not work.")

    def geocode(self, address: str) -> Tuple[float, float]:
        """
        Geocode an address.

        Args:
            address: The address to geocode

        Returns:
            Tuple[float, float]: The latitude and longitude of the address

        Raises:
            GeolocationServiceUnavailableException: If the geolocation service is unavailable
            InvalidCoordinatesException: If the coordinates are invalid
        """
        if not self.api_key:
            raise GeolocationServiceUnavailableException("Google Maps API key not provided")

        try:
            # Import here to avoid dependency if not used
            import googlemaps
            
            # Create client
            gmaps = googlemaps.Client(key=self.api_key)
            
            # Geocode address
            geocode_result = gmaps.geocode(address)
            
            if not geocode_result:
                raise InvalidCoordinatesException(f"Could not geocode address: {address}")
            
            # Get location
            location = geocode_result[0]['geometry']['location']
            
            return location['lat'], location['lng']
        except ImportError:
            logger.error("googlemaps package not installed. Install with pip install googlemaps")
            raise GeolocationServiceUnavailableException("googlemaps package not installed")
        except Exception as e:
            logger.error(f"Error geocoding address: {str(e)}")
            raise GeolocationServiceUnavailableException(f"Error geocoding address: {str(e)}")

    def reverse_geocode(self, latitude: float, longitude: float) -> Dict[str, str]:
        """
        Reverse geocode coordinates.

        Args:
            latitude: The latitude
            longitude: The longitude

        Returns:
            Dict[str, str]: The address components

        Raises:
            GeolocationServiceUnavailableException: If the geolocation service is unavailable
            InvalidCoordinatesException: If the coordinates are invalid
        """
        if not self.api_key:
            raise GeolocationServiceUnavailableException("Google Maps API key not provided")

        try:
            # Import here to avoid dependency if not used
            import googlemaps
            
            # Create client
            gmaps = googlemaps.Client(key=self.api_key)
            
            # Reverse geocode
            reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
            
            if not reverse_geocode_result:
                raise InvalidCoordinatesException(f"Could not reverse geocode coordinates: {latitude}, {longitude}")
            
            # Extract address components
            result = reverse_geocode_result[0]
            address_components = result['address_components']
            
            # Build address dict
            address = {}
            
            # Map Google address components to our model fields
            component_mapping = {
                'street_number': 'street_number',
                'route': 'street',
                'locality': 'city',
                'administrative_area_level_1': 'state',
                'country': 'country',
                'postal_code': 'postal_code'
            }
            
            for component in address_components:
                for component_type in component['types']:
                    if component_type in component_mapping:
                        address[component_mapping[component_type]] = component['long_name']
                        
                        # Also store short name for state and country
                        if component_type == 'administrative_area_level_1':
                            address['state_code'] = component['short_name']
                        elif component_type == 'country':
                            address['country_code'] = component['short_name']
            
            # Combine street number and street
            if 'street_number' in address and 'street' in address:
                address['address'] = f"{address.pop('street_number')} {address.pop('street')}"
            elif 'street' in address:
                address['address'] = address.pop('street')
            
            # Add formatted address
            address['formatted_address'] = result['formatted_address']
            
            return address
        except ImportError:
            logger.error("googlemaps package not installed. Install with pip install googlemaps")
            raise GeolocationServiceUnavailableException("googlemaps package not installed")
        except Exception as e:
            logger.error(f"Error reverse geocoding coordinates: {str(e)}")
            raise GeolocationServiceUnavailableException(f"Error reverse geocoding coordinates: {str(e)}")


def get_geolocation_service() -> Optional[GeolocationServiceInterface]:
    """
    Get the geolocation service.

    Returns:
        GeolocationServiceInterface: The geolocation service or None if not available
    """
    try:
        return GoogleMapsGeolocationService()
    except Exception as e:
        logger.error(f"Error creating geolocation service: {str(e)}")
        return None

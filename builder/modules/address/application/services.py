"""
Services for the address application.
"""
import logging
from typing import Optional, Dict, Any, List, Tuple

from builder.modules.address.application.interfaces import (
    AddressRepositoryInterface,
    GeolocationServiceInterface
)
from builder.modules.address.domain.exceptions import (
    InvalidAddressException,
    AddressNotFoundException,
    GeolocationException
)

logger = logging.getLogger(__name__)


class AddressService:
    """Service for handling address operations."""
    
    def __init__(
        self, 
        address_repository: AddressRepositoryInterface,
        geolocation_service: Optional[GeolocationServiceInterface] = None
    ):
        self.address_repository = address_repository
        self.geolocation_service = geolocation_service
    
    def create_address(self, address_data: Dict[str, Any]) -> Any:
        """
        Create an address.
        
        Args:
            address_data: The address data
            
        Returns:
            The created address object
            
        Raises:
            InvalidAddressException: If the address data is invalid
        """
        try:
            # Validate required fields
            if 'country' not in address_data:
                raise InvalidAddressException("Country is required")
            
            # If geolocation service is available and coordinates are not provided,
            # try to geocode the address
            if (
                self.geolocation_service and 
                'latitude' not in address_data and 
                'longitude' not in address_data
            ):
                try:
                    # Create a temporary address object for geocoding
                    temp_address = type('TempAddress', (), address_data)
                    latitude, longitude = self.geolocation_service.geocode_address(temp_address)
                    address_data['latitude'] = latitude
                    address_data['longitude'] = longitude
                except Exception as e:
                    logger.warning(f"Failed to geocode address: {str(e)}")
                    # Continue without coordinates
            
            return self.address_repository.create_address(address_data)
        except Exception as e:
            logger.error(f"Failed to create address: {str(e)}")
            if isinstance(e, InvalidAddressException):
                raise
            raise InvalidAddressException(f"Failed to create address: {str(e)}")
    
    def get_address(self, address_id: int) -> Any:
        """
        Get an address by ID.
        
        Args:
            address_id: The ID of the address
            
        Returns:
            The address object
            
        Raises:
            AddressNotFoundException: If the address cannot be found
        """
        try:
            return self.address_repository.get_address_by_id(address_id)
        except Exception as e:
            logger.error(f"Failed to get address {address_id}: {str(e)}")
            raise AddressNotFoundException(f"Address with ID {address_id} not found")
    
    def update_address(self, address_id: int, address_data: Dict[str, Any]) -> Any:
        """
        Update an address.
        
        Args:
            address_id: The ID of the address
            address_data: The updated address data
            
        Returns:
            The updated address object
            
        Raises:
            AddressNotFoundException: If the address cannot be found
            InvalidAddressException: If the address data is invalid
        """
        try:
            # Check if the address exists
            self.get_address(address_id)
            
            # If geolocation service is available and coordinates are not provided,
            # but address fields have changed, try to geocode the address
            if (
                self.geolocation_service and 
                'latitude' not in address_data and 
                'longitude' not in address_data and
                any(field in address_data for field in ['address', 'city', 'postal_code', 'country'])
            ):
                try:
                    # Get the current address
                    current_address = self.get_address(address_id)
                    
                    # Create a temporary address object with updated fields for geocoding
                    temp_data = {
                        'address': address_data.get('address', getattr(current_address, 'address', None)),
                        'city': address_data.get('city', getattr(current_address, 'city', None)),
                        'postal_code': address_data.get('postal_code', getattr(current_address, 'postal_code', None)),
                        'country': address_data.get('country', getattr(current_address, 'country', None))
                    }
                    
                    temp_address = type('TempAddress', (), temp_data)
                    latitude, longitude = self.geolocation_service.geocode_address(temp_address)
                    address_data['latitude'] = latitude
                    address_data['longitude'] = longitude
                except Exception as e:
                    logger.warning(f"Failed to geocode updated address: {str(e)}")
                    # Continue without updating coordinates
            
            return self.address_repository.update_address(address_id, address_data)
        except AddressNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Failed to update address {address_id}: {str(e)}")
            if isinstance(e, InvalidAddressException):
                raise
            raise InvalidAddressException(f"Failed to update address: {str(e)}")
    
    def delete_address(self, address_id: int) -> bool:
        """
        Delete an address.
        
        Args:
            address_id: The ID of the address
            
        Returns:
            bool: True if the address was deleted, False otherwise
            
        Raises:
            AddressNotFoundException: If the address cannot be found
        """
        try:
            # Check if the address exists
            self.get_address(address_id)
            
            return self.address_repository.delete_address(address_id)
        except AddressNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Failed to delete address {address_id}: {str(e)}")
            return False
    
    def list_addresses(self, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        List addresses with optional filters.
        
        Args:
            filters: Optional filters for the addresses
            
        Returns:
            A list of address objects
        """
        try:
            return self.address_repository.list_addresses(filters)
        except Exception as e:
            logger.error(f"Failed to list addresses: {str(e)}")
            return []
    
    def geocode_address(self, address_id: int) -> Tuple[float, float]:
        """
        Geocode an address.
        
        Args:
            address_id: The ID of the address
            
        Returns:
            Tuple[float, float]: The latitude and longitude
            
        Raises:
            AddressNotFoundException: If the address cannot be found
            GeolocationException: If the address cannot be geocoded
        """
        if not self.geolocation_service:
            raise GeolocationException("Geolocation service not available")
        
        try:
            address = self.get_address(address_id)
            
            latitude, longitude = self.geolocation_service.geocode_address(address)
            
            # Update the address with the coordinates
            self.update_address(address_id, {
                'latitude': latitude,
                'longitude': longitude
            })
            
            return latitude, longitude
        except AddressNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Failed to geocode address {address_id}: {str(e)}")
            raise GeolocationException(f"Failed to geocode address: {str(e)}")

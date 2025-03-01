"""
Interfaces for the address application.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Tuple


class AddressRepositoryInterface(ABC):
    """Interface for address repository."""
    
    @abstractmethod
    def create_address(self, address_data: Dict[str, Any]) -> Any:
        """Create an address."""
        pass
    
    @abstractmethod
    def get_address_by_id(self, address_id: int) -> Any:
        """Get an address by ID."""
        pass
    
    @abstractmethod
    def update_address(self, address_id: int, address_data: Dict[str, Any]) -> Any:
        """Update an address."""
        pass
    
    @abstractmethod
    def delete_address(self, address_id: int) -> bool:
        """Delete an address."""
        pass
    
    @abstractmethod
    def list_addresses(self, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        """List addresses with optional filters."""
        pass


class GeolocationServiceInterface(ABC):
    """Interface for geolocation service."""
    
    @abstractmethod
    def geocode_address(self, address: Any) -> Tuple[float, float]:
        """
        Convert an address to coordinates.
        
        Args:
            address: The address to geocode
            
        Returns:
            Tuple[float, float]: The latitude and longitude
        """
        pass
    
    @abstractmethod
    def reverse_geocode(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Convert coordinates to an address.
        
        Args:
            latitude: The latitude
            longitude: The longitude
            
        Returns:
            Dict[str, Any]: The address data
        """
        pass

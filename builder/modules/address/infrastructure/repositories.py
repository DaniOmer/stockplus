"""
Repositories for the address application.
"""
import logging
from typing import Optional, Dict, Any, List

from django.db import models

from builder.modules.address.application.interfaces import AddressRepositoryInterface
from builder.modules.address.domain.exceptions import AddressNotFoundException

logger = logging.getLogger(__name__)


class AddressRepository(AddressRepositoryInterface):
    """Repository for address operations."""
    
    def __init__(self, model_class):
        """
        Initialize the repository with a model class.
        
        Args:
            model_class: The model class to use for address operations
        """
        self.model_class = model_class
    
    def create_address(self, address_data: Dict[str, Any]) -> Any:
        """
        Create an address.
        
        Args:
            address_data: The address data
            
        Returns:
            The created address object
        """
        address = self.model_class(**address_data)
        address.save()
        return address
    
    def get_address_by_id(self, address_id: int) -> Any:
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
            return self.model_class.objects.get(id=address_id)
        except self.model_class.DoesNotExist:
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
        """
        address = self.get_address_by_id(address_id)
        
        for key, value in address_data.items():
            setattr(address, key, value)
        
        address.save()
        return address
    
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
        address = self.get_address_by_id(address_id)
        address.delete()
        return True
    
    def list_addresses(self, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        List addresses with optional filters.
        
        Args:
            filters: Optional filters for the addresses
            
        Returns:
            A list of address objects
        """
        queryset = self.model_class.objects.all()
        
        if filters:
            queryset = queryset.filter(**filters)
            
        return list(queryset)


class UserAddressRepository(AddressRepository):
    """Repository for user address operations."""
    
    def __init__(self):
        """Initialize the repository with the UserAddress model."""
        from builder.models import UserAddress
        super().__init__(UserAddress)


class CompanyAddressRepository(AddressRepository):
    """Repository for company address operations."""
    
    def __init__(self):
        """Initialize the repository with the CompanyAddress model."""
        from builder.models import CompanyAddress
        super().__init__(CompanyAddress)

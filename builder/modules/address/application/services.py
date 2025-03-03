"""
Application services for the address application.
This module contains the application services for the address application.
"""

from typing import List, Optional, Tuple

from builder.modules.address.domain.entities.address import Address
from builder.modules.address.domain.exceptions import AddressNotFoundException
from builder.modules.address.application.interfaces import (
    AddressRepositoryInterface,
    GeolocationServiceInterface
)

class AddressService:
    """
    Address service.

    This class implements the application logic for addresses. It uses the address repository
    to access and manipulate address data and enforces business rules.
    """

    def __init__(self, address_repository: AddressRepositoryInterface, 
                 geolocation_service: GeolocationServiceInterface = None):
        """
        Initialize a new AddressService instance.

        Args:
            address_repository: The address repository to use
            geolocation_service: The geolocation service to use (optional)
        """
        self.address_repository = address_repository
        self.geolocation_service = geolocation_service

    def get_address_by_id(self, address_id) -> Optional[Address]:
        """
        Get an address by ID.

        Args:
            address_id: The ID of the address to retrieve

        Returns:
            Address: The address with the given ID or None if not found
        """
        return self.address_repository.get_by_id(address_id)

    def get_addresses_by_user_id(self, user_id) -> List[Address]:
        """
        Get all addresses for a user.

        Args:
            user_id: The ID of the user

        Returns:
            List[Address]: A list of addresses for the user
        """
        return self.address_repository.get_by_user_id(user_id)

    def get_addresses_by_company_id(self, company_id) -> List[Address]:
        """
        Get all addresses for a company.

        Args:
            company_id: The ID of the company

        Returns:
            List[Address]: A list of addresses for the company
        """
        return self.address_repository.get_by_company_id(company_id)

    def create_address(self, **kwargs) -> Address:
        """
        Create a new address.

        Args:
            **kwargs: The address data

        Returns:
            Address: The created address
        """
        address = Address(**kwargs)
        
        # If geolocation service is available, try to geocode the address
        if self.geolocation_service and not (address.latitude and address.longitude):
            try:
                latitude, longitude = self.geolocation_service.geocode(address.get_full_address())
                address.latitude = latitude
                address.longitude = longitude
            except Exception:
                # If geocoding fails, continue without coordinates
                pass
        
        return self.address_repository.save(address)

    def update_address(self, address_id, **kwargs) -> Address:
        """
        Update an address.

        Args:
            address_id: The ID of the address to update
            **kwargs: The address data to update

        Returns:
            Address: The updated address

        Raises:
            AddressNotFoundException: If the address is not found
        """
        address = self.address_repository.get_by_id(address_id)
        if not address:
            raise AddressNotFoundException(f"Address with ID {address_id} not found")
        
        # Update address fields
        for key, value in kwargs.items():
            if hasattr(address, key):
                setattr(address, key, value)
        
        # If geolocation service is available and address has changed, try to geocode the address
        if self.geolocation_service and ('address' in kwargs or 'city' in kwargs or 
                                         'postal_code' in kwargs or 'country' in kwargs):
            try:
                latitude, longitude = self.geolocation_service.geocode(address.get_full_address())
                address.latitude = latitude
                address.longitude = longitude
            except Exception:
                # If geocoding fails, continue without coordinates
                pass
        
        return self.address_repository.save(address)

    def delete_address(self, address_id) -> bool:
        """
        Delete an address.

        Args:
            address_id: The ID of the address to delete

        Returns:
            bool: True if the address was deleted, False otherwise
        """
        return self.address_repository.delete(address_id)

    def geocode_address(self, address_id) -> Tuple[float, float]:
        """
        Geocode an address.

        Args:
            address_id: The ID of the address to geocode

        Returns:
            Tuple[float, float]: The latitude and longitude of the address

        Raises:
            AddressNotFoundException: If the address is not found
        """
        if not self.geolocation_service:
            raise ValueError("Geolocation service is not available")
        
        address = self.address_repository.get_by_id(address_id)
        if not address:
            raise AddressNotFoundException(f"Address with ID {address_id} not found")
        
        latitude, longitude = self.geolocation_service.geocode(address.get_full_address())
        
        # Update address with coordinates
        address.latitude = latitude
        address.longitude = longitude
        self.address_repository.save(address)
        
        return latitude, longitude

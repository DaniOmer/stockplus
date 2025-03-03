"""
Application interfaces for the address application.
This module contains the application interfaces for the address application.
"""

from abc import ABC, abstractmethod

class AddressRepositoryInterface(ABC):
    """
    Address repository interface
    This interface defines the methods that an address repository must implement.
    """

    @abstractmethod
    def get_by_id(self, address_id):
        """
        Get an address by ID.

        Args:
            address_id: The ID of the address to retrieve

        Returns:
            Address: The address with the given ID or None if not found
        """
        pass

    @abstractmethod
    def get_by_user_id(self, user_id):
        """
        Get all addresses for a user.

        Args:
            user_id: The ID of the user

        Returns:
            List[Address]: A list of addresses for the user
        """
        pass

    @abstractmethod
    def get_by_company_id(self, company_id):
        """
        Get all addresses for a company.

        Args:
            company_id: The ID of the company

        Returns:
            List[Address]: A list of addresses for the company
        """
        pass

    @abstractmethod
    def save(self, address):
        """
        Save an address.

        Args:
            address: The address to save

        Returns:
            Address: The saved address
        """
        pass

    @abstractmethod
    def delete(self, address_id):
        """
        Delete an address.

        Args:
            address_id: The ID of the address to delete

        Returns:
            bool: True if the address was deleted, False otherwise
        """
        pass


class GeolocationServiceInterface(ABC):
    """
    Geolocation service interface.

    This interface defines the methods that a geolocation service must implement.
    """

    @abstractmethod
    def geocode(self, address):
        """
        Geocode an address.

        Args:
            address: The address to geocode

        Returns:
            Tuple[float, float]: The latitude and longitude of the address
        """
        pass

    @abstractmethod
    def reverse_geocode(self, latitude, longitude):
        """
        Reverse geocode coordinates.

        Args:
            latitude: The latitude
            longitude: The longitude

        Returns:
            dict: The address components
        """
        pass

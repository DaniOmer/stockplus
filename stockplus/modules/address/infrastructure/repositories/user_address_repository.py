"""
Repositories for the address application.
This module contains the repositories for user address.
"""

from typing import List, Optional

from stockplus.modules.address.application.interfaces import AddressRepositoryInterface
from stockplus.modules.address.infrastructure.models import UserAddress

class UserAddressRepository(AddressRepositoryInterface):
    """
    User address repository implementation.
    This class implements the AddressRepositoryInterface using Django ORM for user addresses.
    """

    def get_by_id(self, address_id) -> Optional[UserAddress]:
        """
        Get a user address by ID.

        Args:
            address_id: The ID of the address to retrieve

        Returns:
            UserAddress: The address with the given ID or None if not found
        """
        try:
            return UserAddress.objects.get(id=address_id)
        except UserAddress.DoesNotExist:
            return None

    def get_by_user_id(self, user_id) -> List[UserAddress]:
        """
        Get all addresses for a user.

        Args:
            user_id: The ID of the user

        Returns:
            List[UserAddress]: A list of addresses for the user
        """
        return list(UserAddress.objects.filter(user_id=user_id))

    def get_by_company_id(self, company_id) -> List[UserAddress]:
        """
        Get all addresses for users in a company.

        Args:
            company_id: The ID of the company

        Returns:
            List[UserAddress]: A list of addresses for users in the company
        """
        return list(UserAddress.objects.filter(user__company_id=company_id))

    def save(self, address) -> UserAddress:
        """
        Save a user address.

        Args:
            address: The address to save

        Returns:
            UserAddress: The saved address
        """
        address.save()
        return address

    def delete(self, address_id) -> bool:
        """
        Delete a user address.

        Args:
            address_id: The ID of the address to delete

        Returns:
            bool: True if the address was deleted, False otherwise
        """
        try:
            address = UserAddress.objects.get(id=address_id)
            address.delete()
            return True
        except UserAddress.DoesNotExist:
            return False

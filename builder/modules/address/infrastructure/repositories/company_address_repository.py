"""
Repositories for the address application.
This module contains the repositories for company address.
"""

from typing import List, Optional

from builder.modules.address.application.interfaces import AddressRepositoryInterface
from builder.models import CompanyAddress

class CompanyAddressRepository(AddressRepositoryInterface):
    """
    Company address repository implementation.
    This class implements the AddressRepositoryInterface using Django ORM for company addresses.
    """

    def get_by_id(self, address_id) -> Optional[CompanyAddress]:
        """
        Get a company address by ID.

        Args:
            address_id: The ID of the address to retrieve

        Returns:
            CompanyAddress: The address with the given ID or None if not found
        """
        try:
            return CompanyAddress.objects.get(id=address_id)
        except CompanyAddress.DoesNotExist:
            return None

    def get_by_user_id(self, user_id) -> List[CompanyAddress]:
        """
        Get all company addresses for a user's company.

        Args:
            user_id: The ID of the user

        Returns:
            List[CompanyAddress]: A list of addresses for the user's company
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(id=user_id)
            if user.company_id:
                return list(CompanyAddress.objects.filter(company_id=user.company_id))
            return []
        except User.DoesNotExist:
            return []

    def get_by_company_id(self, company_id) -> List[CompanyAddress]:
        """
        Get all addresses for a company.

        Args:
            company_id: The ID of the company

        Returns:
            List[CompanyAddress]: A list of addresses for the company
        """
        return list(CompanyAddress.objects.filter(company_id=company_id))

    def save(self, address) -> CompanyAddress:
        """
        Save a company address.

        Args:
            address: The address to save

        Returns:
            CompanyAddress: The saved address
        """
        address.save()
        return address

    def delete(self, address_id) -> bool:
        """
        Delete a company address.

        Args:
            address_id: The ID of the address to delete

        Returns:
            bool: True if the address was deleted, False otherwise
        """
        try:
            address = CompanyAddress.objects.get(id=address_id)
            address.delete()
            return True
        except CompanyAddress.DoesNotExist:
            return False

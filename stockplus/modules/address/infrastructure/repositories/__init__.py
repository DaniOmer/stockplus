"""
Infrastructure layer for the address application.
This package contains repositories implementations for the address application.
"""

from stockplus.modules.address.infrastructure.repositories.user_address_repository import UserAddressRepository
from stockplus.modules.address.infrastructure.repositories.company_address_repository import CompanyAddressRepository

__all__ = [
    UserAddressRepository,
    CompanyAddressRepository
]
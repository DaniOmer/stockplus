"""
Infrastructure layer for the address application.
This package contains repositories implementations for the address application.
"""

from builder.modules.address.infrastructure.repositories.user_address_repository import UserAddressRepository
from builder.modules.address.infrastructure.repositories.company_address_repository import CompanyAddressRepository

__all__ = [
    UserAddressRepository,
    CompanyAddressRepository
]
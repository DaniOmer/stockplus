"""
Infrastructure layer for the address application.
This package contains models implementations for the address application.
"""

from stockplus.modules.address.infrastructure.models.user_address_model import UserAddress
from stockplus.modules.address.infrastructure.models.company_address_model import CompanyAddress


__all__ = [
    UserAddress,
    CompanyAddress
]
"""
Interfaces package.
This package contains the interfaces for the application layer.
"""

from stockplus.modules.pointofsale.application.interfaces import PointOfSaleRepository
from stockplus.modules.pointofsale.application.interfaces import ProductRepository

__all__ = [
    'PointOfSaleRepository',
    'ProductRepository'
]
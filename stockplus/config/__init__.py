"""
Config package.
This package contains the configuration for the application.
"""

from stockplus.config.dependencies import get_service, get_repository

__all__ = [
    'get_service',
    'get_repository'
]

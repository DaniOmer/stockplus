"""
Views for the user application.
This module contains the views for the user application.
"""

from .user import UserViewSet
from .auth import AuthViewSet
from .avatar import AvatarViewSet

__all__ = ['UserViewSet', 'AuthViewSet', 'AvatarViewSet']

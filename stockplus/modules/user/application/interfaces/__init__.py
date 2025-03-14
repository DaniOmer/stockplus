"""
User application interfaces package.
This package contains the interfaces for the user application.
"""

from stockplus.modules.user.application.interfaces.user_repository import IUserRepository
from stockplus.modules.user.application.interfaces.invitation_repository import IInvitationRepository
from stockplus.modules.user.application.interfaces.token_repository import ITokenRepository

__all__ = [
    'IUserRepository',
    'IInvitationRepository',
    'ITokenRepository',
]
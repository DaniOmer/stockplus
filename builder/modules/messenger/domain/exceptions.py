"""
Domain exceptions for the messenger application.
This module contains the domain exceptions for the messenger application.
"""


class MessengerException(Exception):
    """Base exception for messenger-related errors."""
    pass


class MissiveNotFoundException(MessengerException):
    """Exception raised when a missive is not found."""
    pass


class MissiveValidationException(MessengerException):
    """Exception raised when missive validation fails."""
    pass


class MissiveDeliveryException(MessengerException):
    """Exception raised when missive delivery fails."""
    pass


class InvalidMissiveStatusException(MessengerException):
    """Exception raised when an invalid status transition is attempted."""
    pass


class BackendNotFoundException(MessengerException):
    """Exception raised when a backend is not found."""
    pass


class BackendConfigurationException(MessengerException):
    """Exception raised when a backend is misconfigured."""
    pass

"""
Exceptions for the messenger domain.
"""


class MessengerException(Exception):
    """Base exception for messenger module."""
    pass


class MissiveDeliveryException(MessengerException):
    """Exception raised when a missive cannot be delivered."""
    pass


class BackendNotFoundException(MessengerException):
    """Exception raised when a backend cannot be found."""
    pass


class InvalidMissiveStatusException(MessengerException):
    """Exception raised when a missive has an invalid status."""
    pass

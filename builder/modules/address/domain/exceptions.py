"""
Exceptions for the address domain.
"""


class AddressException(Exception):
    """Base exception for address module."""
    pass


class InvalidAddressException(AddressException):
    """Exception raised when an address is invalid."""
    pass


class AddressNotFoundException(AddressException):
    """Exception raised when an address cannot be found."""
    pass


class GeolocationException(AddressException):
    """Exception raised when there is an error with geolocation."""
    pass

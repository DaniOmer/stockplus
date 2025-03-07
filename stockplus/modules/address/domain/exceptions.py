"""
Domain exceptions for the address application.
This module contains the domain exceptions for the address application.
"""


class AddressException(Exception):
    """Base exception for address-related errors."""
    pass


class AddressNotFoundException(AddressException):
    """Exception raised when an address is not found."""
    pass


class AddressValidationException(AddressException):
    """Exception raised when address validation fails."""
    pass


class GeolocationException(AddressException):
    """Exception raised when geolocation fails."""
    pass


class GeolocationServiceUnavailableException(GeolocationException):
    """Exception raised when the geolocation service is unavailable."""
    pass


class InvalidCoordinatesException(GeolocationException):
    """Exception raised when coordinates are invalid."""
    pass

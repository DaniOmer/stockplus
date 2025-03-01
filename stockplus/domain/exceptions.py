"""
Domain exceptions module.
This module contains all the exceptions that can be raised by the domain layer.
"""

class DomainException(Exception):
    """Base exception for all domain exceptions"""
    pass


class UserAlreadyExistsException(DomainException):
    """Exception raised when a user already exists"""
    pass


class InvalidCredentialsException(DomainException):
    """Exception raised when credentials are invalid"""
    pass


class ResourceNotFoundException(DomainException):
    """Exception raised when a resource is not found"""
    pass


class ValidationException(DomainException):
    """Exception raised when validation fails"""
    pass

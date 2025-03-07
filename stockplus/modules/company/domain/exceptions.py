"""
Domain exceptions for the company application.
This module contains the domain exceptions for the company application.
"""


class DomainException(Exception):
    """
    Base exception for all domain exceptions.
    """
    pass


class CompanyNotFoundException(DomainException):
    """
    Exception raised when a company is not found.
    """
    def __init__(self, message="Company not found"):
        self.message = message
        super().__init__(self.message)


class CompanyAlreadyExistsException(DomainException):
    """
    Exception raised when a company already exists.
    """
    def __init__(self, message="Company already exists"):
        self.message = message
        super().__init__(self.message)


class CompanyAddressNotFoundException(DomainException):
    """
    Exception raised when a company address is not found.
    """
    def __init__(self, message="Company address not found"):
        self.message = message
        super().__init__(self.message)


class ValidationException(DomainException):
    """
    Exception raised when validation fails.
    """
    def __init__(self, message="Validation failed"):
        self.message = message
        super().__init__(self.message)

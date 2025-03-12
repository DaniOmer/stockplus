"""
Domain exceptions for the company application.
This module contains the domain exceptions for the company application.
"""
from stockplus.domain.exceptions import DomainException

class CompanyNotFoundException(DomainException):
    """
    Exception raised when a company is not found.
    """
    status_code = 404
    error_type = 'company_not_found'
    default_message = "Company not found"

class CompanyAlreadyExistsException(DomainException):
    """
    Exception raised when a company already exists.
    """
    status_code = 409
    error_type = 'company_already_exists'
    default_message = "Company already exists"

class CompanyAddressNotFoundException(DomainException):
    """
    Exception raised when a company address is not found.
    """
    status_code = 404
    error_type = 'company_address_not_found'
    default_message = "Company address not found"

class ValidationException(DomainException):
    """
    Exception raised when validation fails.
    """
    status_code = 400
    error_type = 'validation_error'
    default_message = "Validation failed"

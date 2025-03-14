"""
User domain exceptions.
This module contains the domain exceptions for the user application.
"""

from stockplus.domain.exceptions import DomainException

class UserNotFoundException(DomainException):
    """
    Exception raised when a user is not found.
    """
    status_code = 404
    error_type = 'user_not_found'
    default_message = "User not found"

class InvalidCredentialsException(DomainException):
    """
    Exception raised when invalid credentials are provided.
    """
    status_code = 401
    error_type = 'invalid_credentials'
    default_message = "Invalid credentials provided"

class TokenInvalidException(DomainException):
    """
    Exception raised when a token is invalid.
    """
    status_code = 401
    error_type = 'invalid_token'
    default_message = "Invalid token"

class TokenExpiredException(DomainException):
    """
    Exception raised when a token has expired.
    """
    status_code = 401
    error_type = 'expired_token'
    default_message = "Token has expired"

class UserAlreadyExistsException(DomainException):
    """
    Exception raised when a user already exists.
    """
    status_code = 409
    error_type = 'user_already_exists'
    default_message = "User already exists"

class UserNotVerifiedException(DomainException):
    """
    Exception raised when a user is not verified.
    """
    status_code = 403
    error_type = 'user_not_verified'
    default_message = "User is not verified"

class InvitationNotFoundException(DomainException):
    """
    Exception raised when an invitation is not found.
    """
    status_code = 404
    error_type = 'invitation_not_found'
    default_message = "Invitation not found"

class InvitationExpiredException(DomainException):
    """
    Exception raised when an invitation has expired.
    """
    status_code = 410
    error_type = 'invitation_expired'
    default_message = "Invitation has expired"

class InvitationAlreadyValidatedException(DomainException):
    """
    Exception raised when an invitation has already been validated.
    """
    status_code = 409
    error_type = 'invitation_already_validated'
    default_message = "Invitation has already been validated"

class ValidationException(DomainException):
    """
    Exception raised when validation fails.
    """
    status_code = 422
    error_type = 'validation_failed'
    default_message = "Validation failed"

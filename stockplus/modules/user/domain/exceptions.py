"""
User domain exceptions.
This module contains the domain exceptions for the user application.
"""


class UserException(Exception):
    """
    Base exception for the user domain.
    """
    pass


class UserNotFoundException(UserException):
    """
    Exception raised when a user is not found.
    """
    pass


class InvalidCredentialsException(UserException):
    """
    Exception raised when invalid credentials are provided.
    """
    pass


class TokenInvalidException(UserException):
    """
    Exception raised when a token is invalid.
    """
    pass


class TokenExpiredException(UserException):
    """
    Exception raised when a token has expired.
    """
    pass


class UserAlreadyExistsException(UserException):
    """
    Exception raised when a user already exists.
    """
    pass


class UserNotVerifiedException(UserException):
    """
    Exception raised when a user is not verified.
    """
    pass


class InvitationNotFoundException(UserException):
    """
    Exception raised when an invitation is not found.
    """
    pass


class InvitationExpiredException(UserException):
    """
    Exception raised when an invitation has expired.
    """
    pass


class InvitationAlreadyValidatedException(UserException):
    """
    Exception raised when an invitation has already been validated.
    """
    pass


class ValidationException(UserException):
    """
    Exception raised when validation fails.
    """
    pass

"""
Domain exceptions for the user application.
This module contains the domain exceptions for the user application.
"""


class UserException(Exception):
    """
    Base exception for user-related errors.
    """
    pass


class UserNotFoundException(UserException):
    """
    Exception raised when a user is not found.
    """
    pass


class UserAlreadyExistsException(UserException):
    """
    Exception raised when a user already exists.
    """
    pass


class ValidationException(UserException):
    """
    Exception raised when validation fails.
    """
    pass


class AuthenticationException(UserException):
    """
    Exception raised when authentication fails.
    """
    pass


class PasswordResetException(UserException):
    """
    Exception raised when a password reset fails.
    """
    pass


class TokenExpiredException(UserException):
    """
    Exception raised when a token has expired.
    """
    pass


class TokenInvalidException(UserException):
    """
    Exception raised when a token is invalid.
    """
    pass


class InvitationException(Exception):
    """
    Base exception for invitation-related errors.
    """
    pass


class InvitationNotFoundException(InvitationException):
    """
    Exception raised when an invitation is not found.
    """
    pass


class InvitationExpiredException(InvitationException):
    """
    Exception raised when an invitation has expired.
    """
    pass


class InvitationAlreadyValidatedException(InvitationException):
    """
    Exception raised when an invitation has already been validated.
    """
    pass

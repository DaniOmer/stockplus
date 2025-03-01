"""
Domain exceptions for the user application.
This module contains the domain exceptions for the user application.
"""


class DomainException(Exception):
    """
    Base exception for all domain exceptions.
    """
    pass


class UserNotFoundException(DomainException):
    """
    Exception raised when a user is not found.
    """
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsException(DomainException):
    """
    Exception raised when a user already exists.
    """
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsException(DomainException):
    """
    Exception raised when credentials are invalid.
    """
    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__(self.message)


class UserNotVerifiedException(DomainException):
    """
    Exception raised when a user is not verified.
    """
    def __init__(self, message="User not verified"):
        self.message = message
        super().__init__(self.message)


class UserNotActiveException(DomainException):
    """
    Exception raised when a user is not active.
    """
    def __init__(self, message="User not active"):
        self.message = message
        super().__init__(self.message)


class InvitationNotFoundException(DomainException):
    """
    Exception raised when an invitation is not found.
    """
    def __init__(self, message="Invitation not found"):
        self.message = message
        super().__init__(self.message)


class InvitationExpiredException(DomainException):
    """
    Exception raised when an invitation has expired.
    """
    def __init__(self, message="Invitation has expired"):
        self.message = message
        super().__init__(self.message)


class InvitationAlreadyValidatedException(DomainException):
    """
    Exception raised when an invitation has already been validated.
    """
    def __init__(self, message="Invitation has already been validated"):
        self.message = message
        super().__init__(self.message)


class ValidationException(DomainException):
    """
    Exception raised when validation fails.
    """
    def __init__(self, message="Validation failed"):
        self.message = message
        super().__init__(self.message)

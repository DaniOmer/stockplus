"""
User domain exceptions.
This module contains the domain exceptions for the user application.
"""

class UserException(Exception):
    """
    Base exception for the user domain.
    """
    error_code = 'user_error'

    def __init__(self, message: str = "An error occurred in the user domain"):
        self.message = message
        super().__init__(message)

class UserNotFoundException(UserException):
    """
    Exception raised when a user is not found.
    """
    error_code = 'user_not_found'

    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(message)

class InvalidCredentialsException(UserException):
    """
    Exception raised when invalid credentials are provided.
    """
    error_code = 'invalid_credentials'

    def __init__(self, message: str = "Invalid credentials provided"):
        self.message = message
        super().__init__(message)

class TokenInvalidException(UserException):
    """
    Exception raised when a token is invalid.
    """
    error_code = 'invalid_token'

    def __init__(self, message: str = "Invalid token"):
        self.message = message
        super().__init__(message)

class TokenExpiredException(UserException):
    """
    Exception raised when a token has expired.
    """
    error_code = 'expired_token'

    def __init__(self, message: str = "Token has expired"):
        self.message = message
        super().__init__(message)

class UserAlreadyExistsException(UserException):
    """
    Exception raised when a user already exists.
    """
    error_code = 'user_already_exists'

    def __init__(self, message: str = "User already exists"):
        self.message = message
        super().__init__(message)

class UserNotVerifiedException(UserException):
    """
    Exception raised when a user is not verified.
    """
    error_code = 'user_not_verified'

    def __init__(self, message: str = "User is not verified"):
        self.message = message
        super().__init__(message)

class InvitationNotFoundException(UserException):
    """
    Exception raised when an invitation is not found.
    """
    error_code = 'invitation_not_found'

    def __init__(self, message: str = "Invitation not found", invitation_id=None):
        self.message = message
        self.invitation_id = invitation_id
        super().__init__(message)

class InvitationExpiredException(UserException):
    """
    Exception raised when an invitation has expired.
    """
    error_code = 'invitation_expired'

    def __init__(self, message: str = "Invitation has expired", expiration_date=None):
        self.message = message
        self.expiration_date = expiration_date
        super().__init__(message)

class InvitationAlreadyValidatedException(UserException):
    """
    Exception raised when an invitation has already been validated.
    """
    error_code = 'invitation_already_validated'

    def __init__(self, message: str = "Invitation has already been validated"):
        self.message = message
        super().__init__(message)

class ValidationException(UserException):
    """
    Exception raised when validation fails.
    """
    error_code = 'validation_failed'

    def __init__(self, message: str = "Validation failed", errors=None):
        if errors:
            self.message = f"Validation failed: {errors}"
        else:
            self.message = message
        super().__init__(message)

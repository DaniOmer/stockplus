"""
Collaborator exceptions.
"""

class CollaboratorException(Exception):
    """Base exception for collaborator module."""
    pass


class CollaboratorNotFound(CollaboratorException):
    """Raised when a collaborator is not found."""
    pass


class RoleNotFound(CollaboratorException):
    """Raised when a role is not found."""
    pass


class PermissionDenied(CollaboratorException):
    """Raised when a collaborator does not have the required permission."""
    pass


class InvalidRole(CollaboratorException):
    """Raised when an invalid role is provided."""
    pass


class InvalidPOS(CollaboratorException):
    """Raised when an invalid point of sale is provided."""
    pass

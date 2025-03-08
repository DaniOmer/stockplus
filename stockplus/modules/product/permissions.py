"""
Permissions for the product module.
"""

from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Permission to check if the user is an admin.
    """
    def has_permission(self, request, view):
        """
        Check if the user is an admin.
        
        Args:
            request: The request object.
            view: The view object.
            
        Returns:
            True if the user is an admin, False otherwise.
        """
        # Check if the user is authenticated and has the admin role
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'role') and 
            request.user.role == 'admin'
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Permission to allow read-only access to all users, but only allow admin users to perform write operations.
    """
    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the requested action.
        
        Args:
            request: The request object.
            view: The view object.
            
        Returns:
            True if the user has permission, False otherwise.
        """
        # Allow GET, HEAD, OPTIONS requests for all authenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated
        
        # Check if the user is an admin for write operations
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'role') and 
            request.user.role == 'admin'
        )

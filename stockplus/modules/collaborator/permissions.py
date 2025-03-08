"""
Collaborator permissions.
This module contains the permission classes for the collaborator module.
"""

from rest_framework import permissions

from stockplus.modules.collaborator.application.services import CollaboratorService
from stockplus.modules.collaborator.infrastructure.repositories import (
    CollaboratorRepository,
    CollaboratorRoleRepository,
)


class HasCollaboratorPermission(permissions.BasePermission):
    """
    Permission class to check if a user has a specific collaborator permission.
    """
    
    def __init__(self, required_permission):
        self.required_permission = required_permission
        self.collaborator_service = None
    
    def has_permission(self, request, view):
        """
        Check if the user has the required permission.
        
        Args:
            request: The request object.
            view: The view object.
            
        Returns:
            True if the user has the required permission, False otherwise.
        """
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if not request.user.company_id:
            return False
        
        if not self.collaborator_service:
            collaborator_repository = CollaboratorRepository()
            role_repository = CollaboratorRoleRepository()
            self.collaborator_service = CollaboratorService(
                collaborator_repository=collaborator_repository,
                role_repository=role_repository,
            )
        
        return self.collaborator_service.check_permission(
            user_id=request.user.id,
            company_id=request.user.company_id,
            permission=self.required_permission,
        )


class HasPOSAccess(permissions.BasePermission):
    """
    Permission class to check if a user has access to a specific point of sale.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user has access to the point of sale.
        
        Args:
            request: The request object.
            view: The view object.
            
        Returns:
            True if the user has access to the point of sale, False otherwise.
        """
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if not request.user.company_id:
            return False
        
        pos_id = view.kwargs.get('pos_id') or request.data.get('point_of_sale')
        if not pos_id:
            return True  # No specific POS to check
        
        collaborator_repository = CollaboratorRepository()
        role_repository = CollaboratorRoleRepository()
        collaborator_service = CollaboratorService(
            collaborator_repository=collaborator_repository,
            role_repository=role_repository,
        )
        
        return collaborator_service.check_pos_access(
            user_id=request.user.id,
            company_id=request.user.company_id,
            pos_id=pos_id,
        )
    

def collaborator_permission_factory(permission_code: str):
    """Fabrique de classes de permission dynamiques"""
    class ConfiguredPermission(HasCollaboratorPermission):
        def __init__(self):
            super().__init__(required_permission=permission_code)
    
    return ConfiguredPermission


# Common permission classes
CanManageCollaborators = collaborator_permission_factory('manage_collaborators')
CanViewCollaborators = collaborator_permission_factory('view_collaborators')
CanManageRoles = collaborator_permission_factory('manage_roles')
CanViewRoles = collaborator_permission_factory('view_roles')
CanManageSales = collaborator_permission_factory('manage_sales')
CanViewSales = collaborator_permission_factory('view_sales')
CanManageProducts = collaborator_permission_factory('manage_products')
CanViewProducts = collaborator_permission_factory('view_products')
CanManageInventory = collaborator_permission_factory('manage_inventory')
CanViewInventory = collaborator_permission_factory('view_inventory')
CanViewReports = collaborator_permission_factory('view_reports')
CanExportData = collaborator_permission_factory('export_data')

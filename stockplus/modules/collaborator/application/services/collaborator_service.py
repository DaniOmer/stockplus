"""
Collaborator service implementation.
This module contains the implementation of the collaborator application services.
"""

from typing import List, Optional, Dict, Any

from stockplus.modules.collaborator.application.interfaces import (
    CollaboratorServiceInterface,
    CollaboratorRoleServiceInterface,
)
from stockplus.modules.collaborator.domain.entities import Collaborator, CollaboratorRole
from stockplus.modules.collaborator.domain.exceptions import (
    CollaboratorNotFound,
    RoleNotFound,
    PermissionDenied,
    InvalidRole,
    InvalidPOS,
)
from stockplus.modules.collaborator.infrastructure.repositories import (
    CollaboratorRepository,
    CollaboratorRoleRepository,
)


class CollaboratorRoleService(CollaboratorRoleServiceInterface):
    """
    Implementation of the collaborator role service.
    """
    
    def __init__(self, role_repository: CollaboratorRoleRepository):
        self.role_repository = role_repository
    
    def create_role(self, company_id: int, name: str, description: str = None,
                  permissions: List[str] = None, role_type: str = 'custom') -> CollaboratorRole:
        """
        Create a new collaborator role.
        
        Args:
            company_id: The ID of the company.
            name: The name of the role.
            description: The description of the role.
            permissions: The list of permission codenames.
            role_type: The type of the role.
            
        Returns:
            The created role entity.
        """
        return self.role_repository.create_role(
            company_id=company_id,
            name=name,
            description=description,
            permissions=permissions,
            role_type=role_type,
        )
    
    def update_role(self, role_id: int, name: str = None, description: str = None,
                  permissions: List[str] = None) -> CollaboratorRole:
        """
        Update an existing collaborator role.
        
        Args:
            role_id: The ID of the role to update.
            name: The new name of the role.
            description: The new description of the role.
            permissions: The new list of permission codenames.
            
        Returns:
            The updated role entity.
        """
        return self.role_repository.update_role(
            role_id=role_id,
            name=name,
            description=description,
            permissions=permissions,
        )
    
    def delete_role(self, role_id: int) -> None:
        """
        Delete a collaborator role.
        
        Args:
            role_id: The ID of the role to delete.
        """
        self.role_repository.delete_role(role_id=role_id)
    
    def get_role(self, role_id: int) -> CollaboratorRole:
        """
        Get a collaborator role by ID.
        
        Args:
            role_id: The ID of the role.
            
        Returns:
            The role entity.
        """
        return self.role_repository.get_role(role_id=role_id)
    
    def get_roles_by_company(self, company_id: int) -> List[CollaboratorRole]:
        """
        Get all roles for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of role entities.
        """
        return self.role_repository.get_roles_by_company(company_id=company_id)
    
    def get_role_permissions(self, role_id: int) -> List[str]:
        """
        Get all permissions for a role.
        
        Args:
            role_id: The ID of the role.
            
        Returns:
            A list of permission codenames.
        """
        return self.role_repository.get_role_permissions(role_id=role_id)


class CollaboratorService(CollaboratorServiceInterface):
    """
    Implementation of the collaborator service.
    """
    
    def __init__(self, collaborator_repository: CollaboratorRepository, role_repository: CollaboratorRoleRepository):
        self.collaborator_repository = collaborator_repository
        self.role_repository = role_repository
    
    def create_collaborator(self, user_id: int, company_id: int, role_id: int = None,
                          pos_ids: List[int] = None) -> Collaborator:
        """
        Create a new collaborator.
        
        Args:
            user_id: The ID of the user.
            company_id: The ID of the company.
            role_id: The ID of the role.
            pos_ids: The list of point of sale IDs.
            
        Returns:
            The created collaborator entity.
        """
        # Validate role if provided
        if role_id:
            try:
                role = self.role_repository.get_role(role_id=role_id)
            except RoleNotFound:
                raise InvalidRole(f"Role with ID {role_id} not found")
        
        return self.collaborator_repository.create_collaborator(
            user_id=user_id,
            company_id=company_id,
            role_id=role_id,
            pos_ids=pos_ids,
        )
    
    def update_collaborator(self, collaborator_id: int, role_id: int = None,
                          pos_ids: List[int] = None, is_active: bool = None) -> Collaborator:
        """
        Update an existing collaborator.
        
        Args:
            collaborator_id: The ID of the collaborator to update.
            role_id: The new role ID.
            pos_ids: The new list of point of sale IDs.
            is_active: The new active status.
            
        Returns:
            The updated collaborator entity.
        """
        # Validate role if provided
        if role_id:
            try:
                role = self.role_repository.get_role(role_id=role_id)
            except RoleNotFound:
                raise InvalidRole(f"Role with ID {role_id} not found")
        
        return self.collaborator_repository.update_collaborator(
            collaborator_id=collaborator_id,
            role_id=role_id,
            pos_ids=pos_ids,
            is_active=is_active,
        )
    
    def delete_collaborator(self, collaborator_id: int) -> None:
        """
        Delete a collaborator.
        
        Args:
            collaborator_id: The ID of the collaborator to delete.
        """
        self.collaborator_repository.delete_collaborator(collaborator_id=collaborator_id)
    
    def get_collaborator(self, collaborator_id: int) -> Collaborator:
        """
        Get a collaborator by ID.
        
        Args:
            collaborator_id: The ID of the collaborator.
            
        Returns:
            The collaborator entity.
        """
        return self.collaborator_repository.get_collaborator(collaborator_id=collaborator_id)
    
    def get_collaborator_by_user(self, user_id: int, company_id: int) -> Collaborator:
        """
        Get a collaborator by user ID and company ID.
        
        Args:
            user_id: The ID of the user.
            company_id: The ID of the company.
            
        Returns:
            The collaborator entity.
        """
        return self.collaborator_repository.get_collaborator_by_user(
            user_id=user_id,
            company_id=company_id,
        )
    
    def get_collaborators_by_company(self, company_id: int) -> List[Collaborator]:
        """
        Get all collaborators for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of collaborator entities.
        """
        return self.collaborator_repository.get_collaborators_by_company(company_id=company_id)
    
    def get_collaborators_by_pos(self, pos_id: int) -> List[Collaborator]:
        """
        Get all collaborators assigned to a point of sale.
        
        Args:
            pos_id: The ID of the point of sale.
            
        Returns:
            A list of collaborator entities.
        """
        return self.collaborator_repository.get_collaborators_by_pos(pos_id=pos_id)
    
    def check_permission(self, user_id: int, company_id: int, permission: str) -> bool:
        """
        Check if a user has a specific permission in a company.
        
        Args:
            user_id: The ID of the user.
            company_id: The ID of the company.
            permission: The permission codename to check.
            
        Returns:
            True if the user has the permission, False otherwise.
        """
        try:
            collaborator = self.collaborator_repository.get_collaborator_by_user(
                user_id=user_id,
                company_id=company_id,
            )
        except CollaboratorNotFound:
            return False
        
        if not collaborator.is_active:
            return False
        
        if not collaborator.role_id:
            return False
        
        try:
            role_permissions = self.role_repository.get_role_permissions(role_id=collaborator.role_id)
        except RoleNotFound:
            return False
        
        return collaborator.has_permission(permission=permission, role_permissions=role_permissions)
    
    def check_pos_access(self, user_id: int, company_id: int, pos_id: int) -> bool:
        """
        Check if a user has access to a specific point of sale in a company.
        
        Args:
            user_id: The ID of the user.
            company_id: The ID of the company.
            pos_id: The ID of the point of sale.
            
        Returns:
            True if the user has access to the point of sale, False otherwise.
        """
        try:
            collaborator = self.collaborator_repository.get_collaborator_by_user(
                user_id=user_id,
                company_id=company_id,
            )
        except CollaboratorNotFound:
            return False
        
        if not collaborator.is_active:
            return False
        
        return collaborator.is_assigned_to_pos(pos_id=pos_id)

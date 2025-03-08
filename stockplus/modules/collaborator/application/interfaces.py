"""
Collaborator application interfaces.
This module contains the interfaces for the collaborator application services.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from stockplus.modules.collaborator.domain.entities import Collaborator, CollaboratorRole


class CollaboratorRoleServiceInterface(ABC):
    """
    Interface for the collaborator role service.
    """
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def delete_role(self, role_id: int) -> None:
        """
        Delete a collaborator role.
        
        Args:
            role_id: The ID of the role to delete.
        """
        pass
    
    @abstractmethod
    def get_role(self, role_id: int) -> CollaboratorRole:
        """
        Get a collaborator role by ID.
        
        Args:
            role_id: The ID of the role.
            
        Returns:
            The role entity.
        """
        pass
    
    @abstractmethod
    def get_roles_by_company(self, company_id: int) -> List[CollaboratorRole]:
        """
        Get all roles for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of role entities.
        """
        pass
    
    @abstractmethod
    def get_role_permissions(self, role_id: int) -> List[str]:
        """
        Get all permissions for a role.
        
        Args:
            role_id: The ID of the role.
            
        Returns:
            A list of permission codenames.
        """
        pass


class CollaboratorServiceInterface(ABC):
    """
    Interface for the collaborator service.
    """
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def delete_collaborator(self, collaborator_id: int) -> None:
        """
        Delete a collaborator.
        
        Args:
            collaborator_id: The ID of the collaborator to delete.
        """
        pass
    
    @abstractmethod
    def get_collaborator(self, collaborator_id: int) -> Collaborator:
        """
        Get a collaborator by ID.
        
        Args:
            collaborator_id: The ID of the collaborator.
            
        Returns:
            The collaborator entity.
        """
        pass
    
    @abstractmethod
    def get_collaborator_by_user(self, user_id: int, company_id: int) -> Collaborator:
        """
        Get a collaborator by user ID and company ID.
        
        Args:
            user_id: The ID of the user.
            company_id: The ID of the company.
            
        Returns:
            The collaborator entity.
        """
        pass
    
    @abstractmethod
    def get_collaborators_by_company(self, company_id: int) -> List[Collaborator]:
        """
        Get all collaborators for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of collaborator entities.
        """
        pass
    
    @abstractmethod
    def get_collaborators_by_pos(self, pos_id: int) -> List[Collaborator]:
        """
        Get all collaborators assigned to a point of sale.
        
        Args:
            pos_id: The ID of the point of sale.
            
        Returns:
            A list of collaborator entities.
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass

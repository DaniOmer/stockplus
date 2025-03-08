"""
Collaborator repository implementation.
This module contains the repository implementation for collaborators and roles.
"""

from typing import List, Optional, Dict, Any
from django.db.models import Q, Count, Sum, F, Prefetch

from stockplus.modules.collaborator.domain.entities import Collaborator, CollaboratorRole
from stockplus.modules.collaborator.domain.exceptions import CollaboratorNotFound, RoleNotFound
from stockplus.modules.collaborator.infrastructure.models import (
    Collaborator as CollaboratorORM,
    CollaboratorRole as CollaboratorRoleORM,
    CollaboratorPermission,
)


class CollaboratorRoleRepository:
    """
    Repository for collaborator roles.
    """
    
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
        role_orm = CollaboratorRoleORM.objects.create(
            company_id=company_id,
            name=name,
            description=description,
            type=role_type,
        )
        
        if permissions:
            permission_objs = CollaboratorPermission.objects.filter(codename__in=permissions)
            role_orm.permissions.set(permission_objs)
        
        return self._to_entity(role_orm)
    
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
            
        Raises:
            RoleNotFound: If the role is not found.
        """
        try:
            role_orm = CollaboratorRoleORM.objects.get(id=role_id)
        except CollaboratorRoleORM.DoesNotExist:
            raise RoleNotFound(f"Role with ID {role_id} not found")
        
        if name:
            role_orm.name = name
        
        if description is not None:
            role_orm.description = description
        
        role_orm.save()
        
        if permissions is not None:
            permission_objs = CollaboratorPermission.objects.filter(codename__in=permissions)
            role_orm.permissions.set(permission_objs)
        
        return self._to_entity(role_orm)
    
    def delete_role(self, role_id: int) -> None:
        """
        Delete a collaborator role.
        
        Args:
            role_id: The ID of the role to delete.
            
        Raises:
            RoleNotFound: If the role is not found.
        """
        try:
            role_orm = CollaboratorRoleORM.objects.get(id=role_id)
        except CollaboratorRoleORM.DoesNotExist:
            raise RoleNotFound(f"Role with ID {role_id} not found")
        
        role_orm.delete()
    
    def get_role(self, role_id: int) -> CollaboratorRole:
        """
        Get a collaborator role by ID.
        
        Args:
            role_id: The ID of the role.
            
        Returns:
            The role entity.
            
        Raises:
            RoleNotFound: If the role is not found.
        """
        try:
            role_orm = CollaboratorRoleORM.objects.prefetch_related('permissions').get(id=role_id)
        except CollaboratorRoleORM.DoesNotExist:
            raise RoleNotFound(f"Role with ID {role_id} not found")
        
        return self._to_entity(role_orm)
    
    def get_roles_by_company(self, company_id: int) -> List[CollaboratorRole]:
        """
        Get all roles for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of role entities.
        """
        roles_orm = CollaboratorRoleORM.objects.filter(company_id=company_id).prefetch_related('permissions')
        return [self._to_entity(role_orm) for role_orm in roles_orm]
    
    def get_role_permissions(self, role_id: int) -> List[str]:
        """
        Get all permissions for a role.
        
        Args:
            role_id: The ID of the role.
            
        Returns:
            A list of permission codenames.
            
        Raises:
            RoleNotFound: If the role is not found.
        """
        try:
            role_orm = CollaboratorRoleORM.objects.prefetch_related('permissions').get(id=role_id)
        except CollaboratorRoleORM.DoesNotExist:
            raise RoleNotFound(f"Role with ID {role_id} not found")
        
        return [permission.codename for permission in role_orm.permissions.all()]
    
    def _to_entity(self, role_orm: CollaboratorRoleORM) -> CollaboratorRole:
        """
        Convert an ORM role to a domain entity.
        
        Args:
            role_orm: The ORM role.
            
        Returns:
            The role entity.
        """
        permissions = [permission.codename for permission in role_orm.permissions.all()]
        
        return CollaboratorRole(
            id=role_orm.id,
            name=role_orm.name,
            description=role_orm.description or "",
            permissions=permissions,
        )


class CollaboratorRepository:
    """
    Repository for collaborators.
    """
    
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
        collaborator_orm = CollaboratorORM.objects.create(
            user_id=user_id,
            company_id=company_id,
            role_id=role_id,
        )
        
        if pos_ids:
            collaborator_orm.points_of_sale.set(pos_ids)
        
        return self._to_entity(collaborator_orm)
    
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
            
        Raises:
            CollaboratorNotFound: If the collaborator is not found.
        """
        try:
            collaborator_orm = CollaboratorORM.objects.get(id=collaborator_id)
        except CollaboratorORM.DoesNotExist:
            raise CollaboratorNotFound(f"Collaborator with ID {collaborator_id} not found")
        
        if role_id is not None:
            collaborator_orm.role_id = role_id
        
        if is_active is not None:
            collaborator_orm.is_active = is_active
        
        collaborator_orm.save()
        
        if pos_ids is not None:
            collaborator_orm.points_of_sale.set(pos_ids)
        
        return self._to_entity(collaborator_orm)
    
    def delete_collaborator(self, collaborator_id: int) -> None:
        """
        Delete a collaborator.
        
        Args:
            collaborator_id: The ID of the collaborator to delete.
            
        Raises:
            CollaboratorNotFound: If the collaborator is not found.
        """
        try:
            collaborator_orm = CollaboratorORM.objects.get(id=collaborator_id)
        except CollaboratorORM.DoesNotExist:
            raise CollaboratorNotFound(f"Collaborator with ID {collaborator_id} not found")
        
        collaborator_orm.delete()
    
    def get_collaborator(self, collaborator_id: int) -> Collaborator:
        """
        Get a collaborator by ID.
        
        Args:
            collaborator_id: The ID of the collaborator.
            
        Returns:
            The collaborator entity.
            
        Raises:
            CollaboratorNotFound: If the collaborator is not found.
        """
        try:
            collaborator_orm = CollaboratorORM.objects.prefetch_related('points_of_sale').get(id=collaborator_id)
        except CollaboratorORM.DoesNotExist:
            raise CollaboratorNotFound(f"Collaborator with ID {collaborator_id} not found")
        
        return self._to_entity(collaborator_orm)
    
    def get_collaborator_by_user(self, user_id: int, company_id: int) -> Collaborator:
        """
        Get a collaborator by user ID and company ID.
        
        Args:
            user_id: The ID of the user.
            company_id: The ID of the company.
            
        Returns:
            The collaborator entity.
            
        Raises:
            CollaboratorNotFound: If the collaborator is not found.
        """
        try:
            collaborator_orm = CollaboratorORM.objects.prefetch_related('points_of_sale').get(
                user_id=user_id, company_id=company_id
            )
        except CollaboratorORM.DoesNotExist:
            raise CollaboratorNotFound(f"Collaborator with user ID {user_id} and company ID {company_id} not found")
        
        return self._to_entity(collaborator_orm)
    
    def get_collaborators_by_company(self, company_id: int) -> List[Collaborator]:
        """
        Get all collaborators for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of collaborator entities.
        """
        collaborators_orm = CollaboratorORM.objects.filter(company_id=company_id).prefetch_related('points_of_sale')
        return [self._to_entity(collaborator_orm) for collaborator_orm in collaborators_orm]
    
    def get_collaborators_by_pos(self, pos_id: int) -> List[Collaborator]:
        """
        Get all collaborators assigned to a point of sale.
        
        Args:
            pos_id: The ID of the point of sale.
            
        Returns:
            A list of collaborator entities.
        """
        collaborators_orm = CollaboratorORM.objects.filter(points_of_sale__id=pos_id).prefetch_related('points_of_sale')
        return [self._to_entity(collaborator_orm) for collaborator_orm in collaborators_orm]
    
    def _to_entity(self, collaborator_orm: CollaboratorORM) -> Collaborator:
        """
        Convert an ORM collaborator to a domain entity.
        
        Args:
            collaborator_orm: The ORM collaborator.
            
        Returns:
            The collaborator entity.
        """
        pos_ids = [pos.id for pos in collaborator_orm.points_of_sale.all()]
        
        return Collaborator(
            id=collaborator_orm.id,
            user_id=collaborator_orm.user_id,
            role_id=collaborator_orm.role_id,
            pos_ids=pos_ids,
            is_active=collaborator_orm.is_active,
        )

"""
Collaborator entity implementation.
This module contains the collaborator entity implementation.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CollaboratorRole:
    """
    Collaborator role entity.
    """
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    permissions: List[str] = None
    
    def __post_init__(self):
        if self.permissions is None:
            self.permissions = []


@dataclass
class Collaborator:
    """
    Collaborator entity.
    """
    id: Optional[int] = None
    user_id: int = None
    role_id: int = None
    pos_ids: List[int] = None
    is_active: bool = True
    
    def __post_init__(self):
        if self.pos_ids is None:
            self.pos_ids = []
    
    def has_permission(self, permission: str, role_permissions: List[str]) -> bool:
        """
        Check if the collaborator has a specific permission.
        
        Args:
            permission: The permission to check.
            role_permissions: The permissions associated with the collaborator's role.
            
        Returns:
            True if the collaborator has the permission, False otherwise.
        """
        return permission in role_permissions
    
    def is_assigned_to_pos(self, pos_id: int) -> bool:
        """
        Check if the collaborator is assigned to a specific point of sale.
        
        Args:
            pos_id: The point of sale ID to check.
            
        Returns:
            True if the collaborator is assigned to the point of sale, False otherwise.
        """
        return pos_id in self.pos_ids

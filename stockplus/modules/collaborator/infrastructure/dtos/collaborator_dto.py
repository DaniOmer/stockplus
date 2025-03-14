"""
Data Transfer Objects (DTOs) for the collaborator application.
This module contains the DTOs for the collaborator application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class CollaboratorRoleBaseDTO(BaseModel):
    """
    Base DTO for collaborator role data.
    Contains common validation rules for collaborator role data.
    """
    
    name: str = Field(..., min_length=1, max_length=100, description="Role name")
    description: Optional[str] = Field(None, max_length=500, description="Role description")
    permissions: Optional[List[str]] = Field(None, description="List of permissions associated with the role")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class CollaboratorRoleCreateDTO(CollaboratorRoleBaseDTO):
    """
    DTO for creating a new collaborator role.
    Inherits validation rules from CollaboratorRoleBaseDTO.
    """
    pass


class CollaboratorRoleUpdateDTO(CollaboratorRoleBaseDTO):
    """
    DTO for updating collaborator role information.
    """
    pass


class CollaboratorRolePartialUpdateDTO(CollaboratorRoleBaseDTO):
    """
    DTO for partially updating collaborator role information.
    All fields are optional.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Role name")


class CollaboratorBaseDTO(BaseModel):
    """
    Base DTO for collaborator data.
    Contains common validation rules for collaborator data.
    """
    
    user_id: int = Field(..., gt=0, description="User ID associated with the collaborator")
    role_id: int = Field(..., gt=0, description="Role ID assigned to the collaborator")
    pos_ids: Optional[List[int]] = Field(None, description="List of point of sale IDs the collaborator is assigned to")
    is_active: Optional[bool] = Field(True, description="Whether the collaborator is active")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('pos_ids')
    def validate_pos_ids(cls, v):
        if v is not None:
            for pos_id in v:
                if pos_id <= 0:
                    raise ValueError('Point of sale IDs must be positive integers')
        return v


class CollaboratorCreateDTO(CollaboratorBaseDTO):
    """
    DTO for creating a new collaborator.
    Inherits validation rules from CollaboratorBaseDTO.
    """
    pass


class CollaboratorUpdateDTO(CollaboratorBaseDTO):
    """
    DTO for updating collaborator information.
    """
    pass


class CollaboratorPartialUpdateDTO(CollaboratorBaseDTO):
    """
    DTO for partially updating collaborator information.
    All fields are optional.
    """
    user_id: Optional[int] = Field(None, gt=0, description="User ID associated with the collaborator")
    role_id: Optional[int] = Field(None, gt=0, description="Role ID assigned to the collaborator")


class CollaboratorAssignPosDTO(BaseModel):
    """
    DTO for assigning a collaborator to points of sale.
    """
    
    pos_ids: List[int] = Field(..., description="List of point of sale IDs to assign the collaborator to")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('pos_ids')
    def validate_pos_ids(cls, v):
        if not v:
            raise ValueError('At least one point of sale ID must be provided')
        for pos_id in v:
            if pos_id <= 0:
                raise ValueError('Point of sale IDs must be positive integers')
        return v


class CollaboratorPermissionCheckDTO(BaseModel):
    """
    DTO for checking if a collaborator has a specific permission.
    """
    
    permission: str = Field(..., description="Permission to check")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }

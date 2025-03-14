"""
Data Transfer Objects (DTOs) for the pointofsale application.
This module contains the DTOs for the pointofsale application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, field_validator, StringConstraints
from typing import List, Optional, Literal
from typing_extensions import Annotated
from uuid import UUID


# Type annotations
PosNameStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=100
    )
]

PosTypeStr = Literal["store", "warehouse", "online"]


class PointOfSaleBaseDTO(BaseModel):
    """
    Base DTO for point of sale data.
    Contains common validation rules for point of sale data.
    """
    
    # Required fields
    name: PosNameStr = Field(..., description="Point of sale name")
    type: PosTypeStr = Field("store", description="Point of sale type (store, warehouse, online)")
    company_id: int = Field(..., gt=0, description="Company ID that owns this point of sale")
    
    # Optional fields
    uid: Optional[UUID] = Field(None, description="Unique identifier")
    opening_hours: Optional[str] = Field(None, max_length=100, description="Opening hours")
    closing_hours: Optional[str] = Field(None, max_length=100, description="Closing hours")
    collaborator_ids: Optional[List[int]] = Field(None, description="List of collaborator IDs assigned to this point of sale")
    is_active: Optional[bool] = Field(True, description="Whether the point of sale is active")
    is_default: Optional[bool] = Field(False, description="Whether this is the default point of sale for the company")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('collaborator_ids')
    def validate_collaborator_ids(cls, v):
        if v is not None:
            for collaborator_id in v:
                if collaborator_id <= 0:
                    raise ValueError('Collaborator IDs must be positive integers')
        return v


class PointOfSaleCreateDTO(PointOfSaleBaseDTO):
    """
    DTO for creating a new point of sale.
    Inherits validation rules from PointOfSaleBaseDTO.
    """
    pass


class PointOfSaleUpdateDTO(PointOfSaleBaseDTO):
    """
    DTO for updating point of sale information.
    """
    pass


class PointOfSalePartialUpdateDTO(PointOfSaleBaseDTO):
    """
    DTO for partially updating point of sale information.
    All fields are optional.
    """
    name: Optional[PosNameStr] = Field(None, description="Point of sale name")
    type: Optional[PosTypeStr] = Field(None, description="Point of sale type (store, warehouse, online)")
    company_id: Optional[int] = Field(None, gt=0, description="Company ID that owns this point of sale")


class PointOfSaleAssignCollaboratorsDTO(BaseModel):
    """
    DTO for assigning collaborators to a point of sale.
    """
    
    collaborator_ids: List[int] = Field(..., description="List of collaborator IDs to assign to the point of sale")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('collaborator_ids')
    def validate_collaborator_ids(cls, v):
        if not v:
            raise ValueError('At least one collaborator ID must be provided')
        for collaborator_id in v:
            if collaborator_id <= 0:
                raise ValueError('Collaborator IDs must be positive integers')
        return v


class PointOfSaleSetDefaultDTO(BaseModel):
    """
    DTO for setting a point of sale as the default for a company.
    """
    
    is_default: bool = Field(..., description="Whether this point of sale should be the default")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }

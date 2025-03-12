"""
Data Transfer Objects (DTOs) for the company application.
This module contains the DTOs for the company application.
DTOs are used to validate and transfer data between layers.
"""

from datetime import date
from pydantic import BaseModel, Field, field_validator, HttpUrl, StringConstraints
from typing_extensions import Annotated, Optional

NAME_PATTERN = r'^[a-zA-Z0-9\s\-\.,&\'()]+$'
LEGAL_FORM_PATTERN = r'^[a-zA-Z0-9\s\-\.]+$'
IDENTIFIER_PATTERN = r'^[a-zA-Z0-9\s\-\.\/]+$'
SIREN_PATTERN = r'^\d{9}$'
SIRET_PATTERN = r'^\d{14}$'

NameStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=255,
        pattern=NAME_PATTERN
    )
]

LegalFormStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=50,
        pattern=LEGAL_FORM_PATTERN
    )
]

IdentifierStr = Annotated[
    str,
    StringConstraints(
        pattern=IDENTIFIER_PATTERN
    )
]

SirenStr = Annotated[
    str,
    StringConstraints(
        pattern=SIREN_PATTERN,
        max_length=9
    )
]

SiretStr = Annotated[
    str,
    StringConstraints(
        pattern=SIRET_PATTERN,
        max_length=14
    )
]

class CompanyBaseDTO(BaseModel):
    """
    Base DTO for company data.
    Contains common validation rules for company data.
    """
    
    # Use StringConstraints to enforce string-only validation with regex pattern
    denomination: NameStr = Field(
        ..., description="Company name (letters, numbers, spaces, and basic punctuation only)"
    )
    legal_form: LegalFormStr = Field(
        ..., description="Legal form of the company (letters, numbers, spaces, hyphens, and dots only)"
    )
    
    # Optional fields
    since: Optional[date] = Field(None, description="Date the company was founded")
    site: Optional[HttpUrl] = Field(None, description="Company website URL")
    effective: Optional[int] = Field(None, ge=0, description="Number of employees (must be positive)")
    resume: Optional[str] = Field(None, max_length=10000, description="Company description")
    
    # Company identifiers with specific validation patterns
    registration_number: Optional[IdentifierStr] = Field(None, max_length=100, description="Company registration number")
    tax_id: Optional[IdentifierStr] = Field(None, max_length=100, description="Company tax ID")
    siren: Optional[SirenStr] = Field(None, description="SIREN number (French companies)")
    siret: Optional[SiretStr] = Field(None, description="SIRET number (French companies)")
    ifu: Optional[IdentifierStr] = Field(None, max_length=100, description="IFU number")
    idu: Optional[IdentifierStr] = Field(None, max_length=100, description="IDU number")
    
    @field_validator('effective')
    def validate_effective(cls, v):
        if v is not None and v < 0:
            raise ValueError('Number of employees must be positive')
        return v
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class CompanyCreateDTO(CompanyBaseDTO):
    """
    DTO for creating a new company.
    Inherits validation rules from CompanyBaseDTO.
    """
    pass


class CompanyUpdateDTO(CompanyBaseDTO):
    """
    DTO for updating company general information.
    """
    pass

class CompanyPartialUpdateDTO(CompanyBaseDTO):
    """
    DTO for partially updating company general information.
    """
    denomination: Optional[NameStr] = Field(
        None, description="Company name (letters, numbers, spaces, and basic punctuation only)"
    )
    legal_form: Optional[LegalFormStr] = Field(
        None, description="Legal form of the company (letters, numbers, spaces, hyphens, and dots only)"
    )

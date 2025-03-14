"""
Data Transfer Objects (DTOs) for the address application.
This module contains the DTOs for the address application.
DTOs are used to validate and transfer data between layers.
"""

from pydantic import BaseModel, Field, StringConstraints, field_validator
from typing_extensions import Annotated, Optional

# Regex patterns for validation
POSTAL_CODE_PATTERN = r'^\d{5}$'  # Basic 5-digit postal code pattern
COUNTRY_CODE_PATTERN = r'^[A-Z]{2}$'  # ISO 3166-1 alpha-2 country code
STATE_CODE_PATTERN = r'^[A-Z]{2}$'  # State/province code (e.g., CA for California)

# Type annotations
PostalCodeStr = Annotated[
    str,
    StringConstraints(
        pattern=POSTAL_CODE_PATTERN
    )
]

CountryCodeStr = Annotated[
    str,
    StringConstraints(
        pattern=COUNTRY_CODE_PATTERN
    )
]

StateCodeStr = Annotated[
    str,
    StringConstraints(
        pattern=STATE_CODE_PATTERN
    )
]

class AddressBaseDTO(BaseModel):
    """
    Base DTO for address data.
    Contains common validation rules for address data.
    """
    
    # Address fields
    address: Optional[str] = Field(None, max_length=255, description="Street address")
    complement: Optional[str] = Field(None, max_length=255, description="Address complement (apartment, suite, etc.)")
    city: Optional[str] = Field(None, max_length=100, description="City name")
    postal_code: Optional[str] = Field(None, max_length=20, description="Postal code")
    state: Optional[str] = Field(None, max_length=100, description="State or province name")
    state_code: Optional[str] = Field(None, max_length=10, description="State or province code")
    country: Optional[str] = Field(None, max_length=100, description="Country name")
    country_code: Optional[str] = Field(None, max_length=2, description="Country code (ISO 3166-1 alpha-2)")
    cedex: Optional[str] = Field(None, max_length=100, description="CEDEX name (French postal service)")
    cedex_code: Optional[str] = Field(None, max_length=20, description="CEDEX code")
    special: Optional[str] = Field(None, max_length=255, description="Special address information")
    index: Optional[str] = Field(None, max_length=50, description="Address index or identifier")
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0, description="Longitude coordinate")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }
    
    @field_validator('latitude')
    def validate_latitude(cls, v):
        if v is not None and (v < -90.0 or v > 90.0):
            raise ValueError('Latitude must be between -90 and 90 degrees')
        return v
    
    @field_validator('longitude')
    def validate_longitude(cls, v):
        if v is not None and (v < -180.0 or v > 180.0):
            raise ValueError('Longitude must be between -180 and 180 degrees')
        return v


class AddressCreateDTO(AddressBaseDTO):
    """
    DTO for creating a new address.
    Inherits validation rules from AddressBaseDTO.
    """
    pass


class AddressUpdateDTO(AddressBaseDTO):
    """
    DTO for updating address information.
    """
    pass


class AddressPartialUpdateDTO(AddressBaseDTO):
    """
    DTO for partially updating address information.
    All fields are optional.
    """
    pass


class GeocodingRequestDTO(BaseModel):
    """
    DTO for geocoding request.
    """
    address: str = Field(..., description="Full address to geocode")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }


class GeocodingResponseDTO(BaseModel):
    """
    DTO for geocoding response.
    """
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    formatted_address: str = Field(..., description="Formatted address")
    
    model_config = {
        "extra": "forbid",  # Forbid extra fields to prevent data injection
    }

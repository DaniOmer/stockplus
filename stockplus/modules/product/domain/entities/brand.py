from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Brand:
    """
    Domain model for a brand.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    name: str = ""
    description: Optional[str] = None
    logo_url: Optional[str] = None
    company_id: int = 0
    is_active: bool = True
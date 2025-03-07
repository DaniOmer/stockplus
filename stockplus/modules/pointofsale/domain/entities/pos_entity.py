from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID


@dataclass
class PointOfSale:
    """
    Domain model for a point of sale.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    name: str = ""
    type: str = "store"
    company_id: int = 0
    opening_hours: Optional[str] = None
    closing_hours: Optional[str] = None
    collaborator_ids: List[int] = field(default_factory=list)
    is_active: bool = True
    is_default: bool = False
    
    @property
    def is_store(self) -> bool:
        return self.type == "store"
    
    @property
    def is_warehouse(self) -> bool:
        return self.type == "warehouse"
    
    @property
    def is_online(self) -> bool:
        return self.type == "online"

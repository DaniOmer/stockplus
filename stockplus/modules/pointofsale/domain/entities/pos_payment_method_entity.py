from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class PosPaymentMethod:
    """
    Domain entity for a point of sale payment method.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    name: str = ""
    description: Optional[str] = None
    point_of_sale_id: int = 0
    is_active: bool = True
    requires_confirmation: bool = False
    confirmation_instructions: Optional[str] = None

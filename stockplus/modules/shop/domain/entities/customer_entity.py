from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Customer:
    """
    Domain model for a customer.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    user_id: int = 0
    stripe_id: Optional[str] = None
    is_active: bool = True

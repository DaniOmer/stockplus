from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from stockplus.modules.sales.domain.entities.sale_item import SaleItem


@dataclass
class Sale:
    """
    Domain model for a sale.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    invoice_number: Optional[str] = None
    date: datetime = field(default_factory=datetime.now)
    total_amount: Decimal = Decimal('0.00')
    payment_method: str = "cash"
    items: List[SaleItem] = field(default_factory=list)
    point_of_sale_id: Optional[int] = None
    company_id: int = 0
    user_id: Optional[int] = None
    is_cancelled: bool = False
    cancelled_at: Optional[datetime] = None
    cancelled_by_id: Optional[int] = None
    notes: Optional[str] = None
    is_active: bool = True
    
    @property
    def item_count(self) -> int:
        """
        Get the total number of items in the sale.
        
        Returns:
            The total number of items.
        """
        return sum(item.quantity for item in self.items)

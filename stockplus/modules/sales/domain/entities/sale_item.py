from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID


@dataclass
class SaleItem:
    """
    Domain model for a sale item.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    sale_id: int = 0
    product_id: int = 0
    product_variant_id: Optional[int] = None
    quantity: int = 1
    unit_price: Decimal = Decimal('0.00')
    discount: Decimal = Decimal('0.00')
    total_price: Decimal = Decimal('0.00')
    is_active: bool = True
    
    def calculate_total(self) -> Decimal:
        """
        Calculate the total price for this item.
        
        Returns:
            The total price.
        """
        return (self.unit_price * Decimal(self.quantity)) - self.discount

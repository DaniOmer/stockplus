from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID


@dataclass
class Invoice:
    """
    Domain model for an invoice.
    """
    id: Optional[int] = None
    uid: Optional[UUID] = None
    invoice_number: str = ""
    sale_id: int = 0
    date: datetime = datetime.now()
    due_date: Optional[datetime] = None
    total_amount: Decimal = Decimal('0.00')
    tax_amount: Decimal = Decimal('0.00')
    discount_amount: Decimal = Decimal('0.00')
    company_id: int = 0
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    notes: Optional[str] = None
    is_paid: bool = False
    payment_date: Optional[datetime] = None
    is_active: bool = True
    
    @property
    def net_amount(self) -> Decimal:
        """
        Calculate the net amount (total - discount).
        
        Returns:
            The net amount.
        """
        return self.total_amount - self.discount_amount
    
    @property
    def grand_total(self) -> Decimal:
        """
        Calculate the grand total (net + tax).
        
        Returns:
            The grand total.
        """
        return self.net_amount + self.tax_amount

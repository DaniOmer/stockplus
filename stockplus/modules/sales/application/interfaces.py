from abc import ABC, abstractmethod
from typing import List, Optional

from stockplus.modules.sales.domain.entities import Sale, SaleItem, Invoice


class ISaleRepository(ABC):
    """
    Interface for the sale repository.
    """
    @abstractmethod
    def get_by_id(self, sale_id: int) -> Optional[Sale]:
        """
        Get a sale by its ID.
        
        Args:
            sale_id: The ID of the sale to retrieve.
            
        Returns:
            The sale, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_invoice_number(self, invoice_number: str) -> Optional[Sale]:
        """
        Get a sale by its invoice number.
        
        Args:
            invoice_number: The invoice number of the sale to retrieve.
            
        Returns:
            The sale, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_company_id(self, company_id: int) -> List[Sale]:
        """
        Get all sales for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of sales for the company.
        """
        pass
    
    @abstractmethod
    def get_by_pos_id(self, pos_id: int) -> List[Sale]:
        """
        Get all sales for a point of sale.
        
        Args:
            pos_id: The ID of the point of sale.
            
        Returns:
            A list of sales for the point of sale.
        """
        pass
    
    @abstractmethod
    def create(self, sale: Sale) -> Sale:
        """
        Create a new sale.
        
        Args:
            sale: The sale to create.
            
        Returns:
            The created sale.
        """
        pass
    
    @abstractmethod
    def update(self, sale: Sale) -> Sale:
        """
        Update an existing sale.
        
        Args:
            sale: The sale to update.
            
        Returns:
            The updated sale.
        """
        pass
    
    @abstractmethod
    def delete(self, sale_id: int) -> None:
        """
        Delete a sale.
        
        Args:
            sale_id: The ID of the sale to delete.
        """
        pass
    
    @abstractmethod
    def add_item(self, sale_id: int, item: SaleItem) -> SaleItem:
        """
        Add an item to a sale.
        
        Args:
            sale_id: The ID of the sale.
            item: The item to add.
            
        Returns:
            The added item.
        """
        pass
    
    @abstractmethod
    def update_item(self, item: SaleItem) -> SaleItem:
        """
        Update a sale item.
        
        Args:
            item: The item to update.
            
        Returns:
            The updated item.
        """
        pass
    
    @abstractmethod
    def delete_item(self, item_id: int) -> None:
        """
        Delete a sale item.
        
        Args:
            item_id: The ID of the item to delete.
        """
        pass
    
    @abstractmethod
    def cancel_sale(self, sale_id: int, user_id: int) -> Sale:
        """
        Cancel a sale.
        
        Args:
            sale_id: The ID of the sale to cancel.
            user_id: The ID of the user who is cancelling the sale.
            
        Returns:
            The cancelled sale.
        """
        pass


class IInvoiceRepository(ABC):
    """
    Interface for the invoice repository.
    """
    @abstractmethod
    def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """
        Get an invoice by its ID.
        
        Args:
            invoice_id: The ID of the invoice to retrieve.
            
        Returns:
            The invoice, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_invoice_number(self, invoice_number: str) -> Optional[Invoice]:
        """
        Get an invoice by its invoice number.
        
        Args:
            invoice_number: The invoice number of the invoice to retrieve.
            
        Returns:
            The invoice, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_sale_id(self, sale_id: int) -> Optional[Invoice]:
        """
        Get an invoice by its sale ID.
        
        Args:
            sale_id: The ID of the sale.
            
        Returns:
            The invoice, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_company_id(self, company_id: int) -> List[Invoice]:
        """
        Get all invoices for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of invoices for the company.
        """
        pass
    
    @abstractmethod
    def create(self, invoice: Invoice) -> Invoice:
        """
        Create a new invoice.
        
        Args:
            invoice: The invoice to create.
            
        Returns:
            The created invoice.
        """
        pass
    
    @abstractmethod
    def update(self, invoice: Invoice) -> Invoice:
        """
        Update an existing invoice.
        
        Args:
            invoice: The invoice to update.
            
        Returns:
            The updated invoice.
        """
        pass
    
    @abstractmethod
    def delete(self, invoice_id: int) -> None:
        """
        Delete an invoice.
        
        Args:
            invoice_id: The ID of the invoice to delete.
        """
        pass
    
    @abstractmethod
    def mark_as_paid(self, invoice_id: int) -> Invoice:
        """
        Mark an invoice as paid.
        
        Args:
            invoice_id: The ID of the invoice to mark as paid.
            
        Returns:
            The updated invoice.
        """
        pass

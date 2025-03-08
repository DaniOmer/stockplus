from typing import List, Optional

from stockplus.modules.sales.application.interfaces import IInvoiceRepository
from stockplus.modules.sales.domain.entities import Invoice
from stockplus.modules.sales.domain.exceptions import InvoiceNotFoundError
from stockplus.modules.sales.infrastructure.utils import generate_pdf_invoice


class InvoiceService:
    """
    Service for managing invoices.
    """
    def __init__(self, invoice_repository: IInvoiceRepository):
        self.invoice_repository = invoice_repository
    
    def get_invoice(self, invoice_id: int) -> Invoice:
        """
        Get an invoice by its ID.
        
        Args:
            invoice_id: The ID of the invoice to retrieve.
            
        Returns:
            The invoice.
            
        Raises:
            InvoiceNotFoundError: If the invoice is not found.
        """
        invoice = self.invoice_repository.get_by_id(invoice_id)
        if not invoice:
            raise InvoiceNotFoundError(invoice_id)
        return invoice
    
    def get_invoice_by_number(self, invoice_number: str) -> Invoice:
        """
        Get an invoice by its invoice number.
        
        Args:
            invoice_number: The invoice number of the invoice to retrieve.
            
        Returns:
            The invoice.
            
        Raises:
            InvoiceNotFoundError: If the invoice is not found.
        """
        invoice = self.invoice_repository.get_by_invoice_number(invoice_number)
        if not invoice:
            raise InvoiceNotFoundError(f"Invoice with number {invoice_number} not found.")
        return invoice
    
    def get_invoice_by_sale(self, sale_id: int) -> Invoice:
        """
        Get an invoice by its sale ID.
        
        Args:
            sale_id: The ID of the sale.
            
        Returns:
            The invoice.
            
        Raises:
            InvoiceNotFoundError: If the invoice is not found.
        """
        invoice = self.invoice_repository.get_by_sale_id(sale_id)
        if not invoice:
            raise InvoiceNotFoundError(f"Invoice for sale with ID {sale_id} not found.")
        return invoice
    
    def get_company_invoices(self, company_id: int) -> List[Invoice]:
        """
        Get all invoices for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of invoices for the company.
        """
        return self.invoice_repository.get_by_company_id(company_id)
    
    def update_invoice(self, 
                      invoice_id: int,
                      due_date: Optional[str] = None,
                      tax_amount: Optional[float] = None,
                      discount_amount: Optional[float] = None,
                      customer_name: Optional[str] = None,
                      customer_email: Optional[str] = None,
                      customer_phone: Optional[str] = None,
                      customer_address: Optional[str] = None,
                      notes: Optional[str] = None) -> Invoice:
        """
        Update an invoice.
        
        Args:
            invoice_id: The ID of the invoice to update.
            due_date: The new due date of the invoice.
            tax_amount: The new tax amount of the invoice.
            discount_amount: The new discount amount of the invoice.
            customer_name: The new name of the customer.
            customer_email: The new email of the customer.
            customer_phone: The new phone number of the customer.
            customer_address: The new address of the customer.
            notes: The new notes for the invoice.
            
        Returns:
            The updated invoice.
            
        Raises:
            InvoiceNotFoundError: If the invoice is not found.
        """
        # Get the current invoice
        invoice = self.get_invoice(invoice_id)
        
        # Update the invoice
        if due_date is not None:
            invoice.due_date = due_date
        
        if tax_amount is not None:
            invoice.tax_amount = tax_amount
        
        if discount_amount is not None:
            invoice.discount_amount = discount_amount
        
        if customer_name is not None:
            invoice.customer_name = customer_name
        
        if customer_email is not None:
            invoice.customer_email = customer_email
        
        if customer_phone is not None:
            invoice.customer_phone = customer_phone
        
        if customer_address is not None:
            invoice.customer_address = customer_address
        
        if notes is not None:
            invoice.notes = notes
        
        # Update the invoice
        return self.invoice_repository.update(invoice)
    
    def mark_as_paid(self, invoice_id: int) -> Invoice:
        """
        Mark an invoice as paid.
        
        Args:
            invoice_id: The ID of the invoice to mark as paid.
            
        Returns:
            The updated invoice.
            
        Raises:
            InvoiceNotFoundError: If the invoice is not found.
        """
        return self.invoice_repository.mark_as_paid(invoice_id)
    
    def generate_pdf(self, invoice_id: int) -> Optional[str]:
        """
        Generate a PDF for an invoice.
        
        Args:
            invoice_id: The ID of the invoice to generate a PDF for.
            
        Returns:
            The path to the generated PDF, or None if the invoice is not found.
            
        Raises:
            InvoiceNotFoundError: If the invoice is not found.
        """
        # Check if the invoice exists
        self.get_invoice(invoice_id)
        
        # Generate the PDF
        return generate_pdf_invoice(invoice_id)

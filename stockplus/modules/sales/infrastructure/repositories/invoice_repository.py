from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from django.db import transaction
from django.utils import timezone

from stockplus.modules.sales.application.interfaces import IInvoiceRepository
from stockplus.modules.sales.domain.entities import Invoice
from stockplus.modules.sales.domain.exceptions import InvoiceNotFoundError
from stockplus.modules.sales.infrastructure.models import Invoice as InvoiceORM


class InvoiceRepository(IInvoiceRepository):
    """
    Implementation of the invoice repository.
    """
    def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """
        Get an invoice by its ID.
        
        Args:
            invoice_id: The ID of the invoice to retrieve.
            
        Returns:
            The invoice, or None if not found.
        """
        try:
            invoice_orm = InvoiceORM.objects.get(id=invoice_id)
            return self._to_domain(invoice_orm)
        except InvoiceORM.DoesNotExist:
            return None
    
    def get_by_invoice_number(self, invoice_number: str) -> Optional[Invoice]:
        """
        Get an invoice by its invoice number.
        
        Args:
            invoice_number: The invoice number of the invoice to retrieve.
            
        Returns:
            The invoice, or None if not found.
        """
        try:
            invoice_orm = InvoiceORM.objects.get(invoice_number=invoice_number)
            return self._to_domain(invoice_orm)
        except InvoiceORM.DoesNotExist:
            return None
    
    def get_by_sale_id(self, sale_id: int) -> Optional[Invoice]:
        """
        Get an invoice by its sale ID.
        
        Args:
            sale_id: The ID of the sale.
            
        Returns:
            The invoice, or None if not found.
        """
        try:
            invoice_orm = InvoiceORM.objects.get(sale_id=sale_id)
            return self._to_domain(invoice_orm)
        except InvoiceORM.DoesNotExist:
            return None
    
    def get_by_company_id(self, company_id: int) -> List[Invoice]:
        """
        Get all invoices for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of invoices for the company.
        """
        invoices_orm = InvoiceORM.objects.filter(company_id=company_id)
        return [self._to_domain(invoice_orm) for invoice_orm in invoices_orm]
    
    @transaction.atomic
    def create(self, invoice: Invoice) -> Invoice:
        """
        Create a new invoice.
        
        Args:
            invoice: The invoice to create.
            
        Returns:
            The created invoice.
        """
        invoice_orm = InvoiceORM(
            uid=uuid4() if not invoice.uid else invoice.uid,
            invoice_number=invoice.invoice_number,
            sale_id=invoice.sale_id,
            due_date=invoice.due_date,
            total_amount=invoice.total_amount,
            tax_amount=invoice.tax_amount,
            discount_amount=invoice.discount_amount,
            company_id=invoice.company_id,
            customer_name=invoice.customer_name,
            customer_email=invoice.customer_email,
            customer_phone=invoice.customer_phone,
            customer_address=invoice.customer_address,
            notes=invoice.notes,
            is_paid=invoice.is_paid,
            payment_date=invoice.payment_date
        )
        invoice_orm.save()
        
        return self._to_domain(invoice_orm)
    
    @transaction.atomic
    def update(self, invoice: Invoice) -> Invoice:
        """
        Update an existing invoice.
        
        Args:
            invoice: The invoice to update.
            
        Returns:
            The updated invoice.
            
        Raises:
            InvoiceNotFoundError: If the invoice is not found.
        """
        try:
            invoice_orm = InvoiceORM.objects.get(id=invoice.id)
        except InvoiceORM.DoesNotExist:
            raise InvoiceNotFoundError(invoice.id)
        
        # Update the invoice
        invoice_orm.invoice_number = invoice.invoice_number
        invoice_orm.due_date = invoice.due_date
        invoice_orm.total_amount = invoice.total_amount
        invoice_orm.tax_amount = invoice.tax_amount
        invoice_orm.discount_amount = invoice.discount_amount
        invoice_orm.customer_name = invoice.customer_name
        invoice_orm.customer_email = invoice.customer_email
        invoice_orm.customer_phone = invoice.customer_phone
        invoice_orm.customer_address = invoice.customer_address
        invoice_orm.notes = invoice.notes
        invoice_orm.is_paid = invoice.is_paid
        invoice_orm.payment_date = invoice.payment_date
        invoice_orm.save()
        
        return self._to_domain(invoice_orm)
    
    @transaction.atomic
    def delete(self, invoice_id: int) -> None:
        """
        Delete an invoice.
        
        Args:
            invoice_id: The ID of the invoice to delete.
            
        Raises:
            InvoiceNotFoundError: If the invoice is not found.
        """
        try:
            invoice_orm = InvoiceORM.objects.get(id=invoice_id)
        except InvoiceORM.DoesNotExist:
            raise InvoiceNotFoundError(invoice_id)
        
        # Delete the invoice
        invoice_orm.delete()
    
    @transaction.atomic
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
        try:
            invoice_orm = InvoiceORM.objects.get(id=invoice_id)
        except InvoiceORM.DoesNotExist:
            raise InvoiceNotFoundError(invoice_id)
        
        # Mark the invoice as paid
        invoice_orm.is_paid = True
        invoice_orm.payment_date = timezone.now()
        invoice_orm.save()
        
        return self._to_domain(invoice_orm)
    
    def _to_domain(self, invoice_orm: InvoiceORM) -> Invoice:
        """
        Convert an ORM invoice to a domain invoice.
        
        Args:
            invoice_orm: The ORM invoice to convert.
            
        Returns:
            The domain invoice.
        """
        return Invoice(
            id=invoice_orm.id,
            uid=invoice_orm.uid,
            invoice_number=invoice_orm.invoice_number,
            sale_id=invoice_orm.sale_id,
            date=invoice_orm.date,
            due_date=invoice_orm.due_date,
            total_amount=invoice_orm.total_amount,
            tax_amount=invoice_orm.tax_amount,
            discount_amount=invoice_orm.discount_amount,
            company_id=invoice_orm.company_id,
            customer_name=invoice_orm.customer_name,
            customer_email=invoice_orm.customer_email,
            customer_phone=invoice_orm.customer_phone,
            customer_address=invoice_orm.customer_address,
            notes=invoice_orm.notes,
            is_paid=invoice_orm.is_paid,
            payment_date=invoice_orm.payment_date,
            is_active=invoice_orm.is_active
        )

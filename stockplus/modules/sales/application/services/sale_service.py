from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from stockplus.modules.product.application.services import ProductService
from stockplus.modules.sales.application.interfaces import ISaleRepository, IInvoiceRepository
from stockplus.modules.sales.domain.entities import Sale, SaleItem, Invoice
from stockplus.modules.sales.domain.exceptions import (
    SaleNotFoundError, SaleItemNotFoundError, 
    SaleAlreadyCancelledError, InsufficientStockError,
    DuplicateSaleError
)
from stockplus.modules.sales.infrastructure.utils import generate_invoice_number


class SaleService:
    """
    Service for managing sales.
    """
    def __init__(self, 
                sale_repository: ISaleRepository,
                invoice_repository: IInvoiceRepository,
                product_service: ProductService):
        self.sale_repository = sale_repository
        self.invoice_repository = invoice_repository
        self.product_service = product_service
    
    def get_sale(self, sale_id: int) -> Sale:
        """
        Get a sale by its ID.
        
        Args:
            sale_id: The ID of the sale to retrieve.
            
        Returns:
            The sale.
            
        Raises:
            SaleNotFoundError: If the sale is not found.
        """
        sale = self.sale_repository.get_by_id(sale_id)
        if not sale:
            raise SaleNotFoundError(sale_id)
        return sale
    
    def get_sale_by_invoice_number(self, invoice_number: str) -> Sale:
        """
        Get a sale by its invoice number.
        
        Args:
            invoice_number: The invoice number of the sale to retrieve.
            
        Returns:
            The sale.
            
        Raises:
            SaleNotFoundError: If the sale is not found.
        """
        sale = self.sale_repository.get_by_invoice_number(invoice_number)
        if not sale:
            raise SaleNotFoundError(f"Sale with invoice number {invoice_number} not found.")
        return sale
    
    def get_company_sales(self, company_id: int) -> List[Sale]:
        """
        Get all sales for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of sales for the company.
        """
        return self.sale_repository.get_by_company_id(company_id)
    
    def get_pos_sales(self, pos_id: int) -> List[Sale]:
        """
        Get all sales for a point of sale.
        
        Args:
            pos_id: The ID of the point of sale.
            
        Returns:
            A list of sales for the point of sale.
        """
        return self.sale_repository.get_by_pos_id(pos_id)
    
    def create_sale(self, 
                   company_id: int,
                   items: List[dict],
                   payment_method: str = "cash",
                   point_of_sale_id: Optional[int] = None,
                   user_id: Optional[int] = None,
                   notes: Optional[str] = None,
                   customer_name: Optional[str] = None,
                   customer_email: Optional[str] = None,
                   customer_phone: Optional[str] = None,
                   customer_address: Optional[str] = None,
                   generate_invoice: bool = True) -> Sale:
        """
        Create a new sale.
        
        Args:
            company_id: The ID of the company.
            items: A list of dictionaries containing item details (product_id, quantity, etc.).
            payment_method: The payment method.
            point_of_sale_id: The ID of the point of sale.
            user_id: The ID of the user who made the sale.
            notes: Additional notes for the sale.
            customer_name: The name of the customer.
            customer_email: The email of the customer.
            customer_phone: The phone number of the customer.
            customer_address: The address of the customer.
            generate_invoice: Whether to generate an invoice for the sale.
            
        Returns:
            The created sale.
            
        Raises:
            InsufficientStockError: If there is insufficient stock for a product.
        """
        # Generate invoice number
        invoice_number = generate_invoice_number(company_id)
        
        # Check if a sale with this invoice number already exists
        existing_sale = self.sale_repository.get_by_invoice_number(invoice_number)
        if existing_sale:
            raise DuplicateSaleError(invoice_number)
        
        # Create sale items
        sale_items = []
        total_amount = Decimal('0.00')
        
        for item_data in items:
            product_id = item_data['product_id']
            quantity = item_data.get('quantity', 1)
            product_variant_id = item_data.get('product_variant_id')
            
            # Get product details
            product = self.product_service.get_product(product_id)
            
            # Determine price
            if product_variant_id:
                # Find the variant
                variant = next((v for v in product.variants if v.id == product_variant_id), None)
                if variant:
                    unit_price = variant.price
                else:
                    # Fallback to product price if variant not found
                    unit_price = Decimal('0.00')  # Product entity doesn't have a price field
            else:
                # Use product price
                unit_price = Decimal('0.00')  # Product entity doesn't have a price field
            
            # Apply discount if any
            discount = Decimal(str(item_data.get('discount', '0.00')))
            
            # Create sale item
            sale_item = SaleItem(
                product_id=product_id,
                product_variant_id=product_variant_id,
                quantity=quantity,
                unit_price=unit_price,
                discount=discount
            )
            
            # Calculate total price for this item
            item_total = sale_item.calculate_total()
            sale_item.total_price = item_total
            
            # Add to total amount
            total_amount += item_total
            
            # Add to sale items
            sale_items.append(sale_item)
        
        # Create the sale
        sale = Sale(
            invoice_number=invoice_number,
            total_amount=total_amount,
            payment_method=payment_method,
            items=sale_items,
            point_of_sale_id=point_of_sale_id,
            company_id=company_id,
            user_id=user_id,
            notes=notes
        )
        
        # Save the sale
        created_sale = self.sale_repository.create(sale)
        
        # Generate invoice if requested
        if generate_invoice:
            self._generate_invoice(
                created_sale,
                customer_name,
                customer_email,
                customer_phone,
                customer_address
            )
        
        return created_sale
    
    def cancel_sale(self, sale_id: int, user_id: int) -> Sale:
        """
        Cancel a sale.
        
        Args:
            sale_id: The ID of the sale to cancel.
            user_id: The ID of the user who is cancelling the sale.
            
        Returns:
            The cancelled sale.
            
        Raises:
            SaleNotFoundError: If the sale is not found.
            SaleAlreadyCancelledError: If the sale is already cancelled.
        """
        return self.sale_repository.cancel_sale(sale_id, user_id)
    
    def add_item_to_sale(self, 
                        sale_id: int,
                        product_id: int,
                        quantity: int = 1,
                        product_variant_id: Optional[int] = None,
                        unit_price: Optional[Decimal] = None,
                        discount: Decimal = Decimal('0.00')) -> SaleItem:
        """
        Add an item to a sale.
        
        Args:
            sale_id: The ID of the sale.
            product_id: The ID of the product.
            quantity: The quantity of the product.
            product_variant_id: The ID of the product variant.
            unit_price: The unit price of the product.
            discount: The discount for the item.
            
        Returns:
            The added item.
            
        Raises:
            SaleNotFoundError: If the sale is not found.
            InsufficientStockError: If there is insufficient stock for the product.
        """
        # Get the sale
        sale = self.get_sale(sale_id)
        
        # Get product details
        product = self.product_service.get_product(product_id)
        
        # Determine price if not provided
        if unit_price is None:
            if product_variant_id:
                # Find the variant
                variant = next((v for v in product.variants if v.id == product_variant_id), None)
                if variant:
                    unit_price = variant.price
                else:
                    # Fallback to product price if variant not found
                    unit_price = Decimal('0.00')  # Product entity doesn't have a price field
            else:
                # Use product price
                unit_price = Decimal('0.00')  # Product entity doesn't have a price field
        
        # Create sale item
        sale_item = SaleItem(
            sale_id=sale_id,
            product_id=product_id,
            product_variant_id=product_variant_id,
            quantity=quantity,
            unit_price=unit_price,
            discount=discount
        )
        
        # Calculate total price
        sale_item.total_price = sale_item.calculate_total()
        
        # Add the item to the sale
        return self.sale_repository.add_item(sale_id, sale_item)
    
    def update_sale_item(self, 
                        item_id: int,
                        quantity: Optional[int] = None,
                        unit_price: Optional[Decimal] = None,
                        discount: Optional[Decimal] = None) -> SaleItem:
        """
        Update a sale item.
        
        Args:
            item_id: The ID of the item to update.
            quantity: The new quantity of the product.
            unit_price: The new unit price of the product.
            discount: The new discount for the item.
            
        Returns:
            The updated item.
            
        Raises:
            SaleItemNotFoundError: If the item is not found.
            InsufficientStockError: If there is insufficient stock for the product.
        """
        # Get the current item
        item = self.sale_repository.get_item(item_id)
        if not item:
            raise SaleItemNotFoundError(item_id)
        
        # Update the item
        if quantity is not None:
            item.quantity = quantity
        
        if unit_price is not None:
            item.unit_price = unit_price
        
        if discount is not None:
            item.discount = discount
        
        # Calculate total price
        item.total_price = item.calculate_total()
        
        # Update the item
        return self.sale_repository.update_item(item)
    
    def remove_sale_item(self, item_id: int) -> None:
        """
        Remove an item from a sale.
        
        Args:
            item_id: The ID of the item to remove.
            
        Raises:
            SaleItemNotFoundError: If the item is not found.
        """
        self.sale_repository.delete_item(item_id)
    
    def _generate_invoice(self, 
                         sale: Sale,
                         customer_name: Optional[str] = None,
                         customer_email: Optional[str] = None,
                         customer_phone: Optional[str] = None,
                         customer_address: Optional[str] = None) -> Invoice:
        """
        Generate an invoice for a sale.
        
        Args:
            sale: The sale to generate an invoice for.
            customer_name: The name of the customer.
            customer_email: The email of the customer.
            customer_phone: The phone number of the customer.
            customer_address: The address of the customer.
            
        Returns:
            The generated invoice.
        """
        # Create the invoice
        invoice = Invoice(
            invoice_number=sale.invoice_number,
            sale_id=sale.id,
            total_amount=sale.total_amount,
            company_id=sale.company_id,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_address=customer_address
        )
        
        # Save the invoice
        return self.invoice_repository.create(invoice)

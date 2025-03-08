from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from django.db import transaction
from django.utils import timezone

from stockplus.modules.product.infrastructure.models import Product
from stockplus.modules.sales.application.interfaces import ISaleRepository
from stockplus.modules.sales.domain.entities import Sale, SaleItem
from stockplus.modules.sales.domain.exceptions import (
    SaleNotFoundError, SaleItemNotFoundError, 
    SaleAlreadyCancelledError, InsufficientStockError
)
from stockplus.modules.sales.infrastructure.models import Sale as SaleORM
from stockplus.modules.sales.infrastructure.models import SaleItem as SaleItemORM


class SaleRepository(ISaleRepository):
    """
    Implementation of the sale repository.
    """
    def get_by_id(self, sale_id: int) -> Optional[Sale]:
        """
        Get a sale by its ID.
        
        Args:
            sale_id: The ID of the sale to retrieve.
            
        Returns:
            The sale, or None if not found.
        """
        try:
            sale_orm = SaleORM.objects.get(id=sale_id)
            return self._to_domain(sale_orm)
        except SaleORM.DoesNotExist:
            return None
    
    def get_by_invoice_number(self, invoice_number: str) -> Optional[Sale]:
        """
        Get a sale by its invoice number.
        
        Args:
            invoice_number: The invoice number of the sale to retrieve.
            
        Returns:
            The sale, or None if not found.
        """
        try:
            sale_orm = SaleORM.objects.get(invoice_number=invoice_number)
            return self._to_domain(sale_orm)
        except SaleORM.DoesNotExist:
            return None
    
    def get_by_company_id(self, company_id: int) -> List[Sale]:
        """
        Get all sales for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of sales for the company.
        """
        sales_orm = SaleORM.objects.filter(company_id=company_id)
        return [self._to_domain(sale_orm) for sale_orm in sales_orm]
    
    def get_by_pos_id(self, pos_id: int) -> List[Sale]:
        """
        Get all sales for a point of sale.
        
        Args:
            pos_id: The ID of the point of sale.
            
        Returns:
            A list of sales for the point of sale.
        """
        sales_orm = SaleORM.objects.filter(point_of_sale_id=pos_id)
        return [self._to_domain(sale_orm) for sale_orm in sales_orm]
    
    @transaction.atomic
    def create(self, sale: Sale) -> Sale:
        """
        Create a new sale.
        
        Args:
            sale: The sale to create.
            
        Returns:
            The created sale.
            
        Raises:
            InsufficientStockError: If there is insufficient stock for a product.
        """
        # Check stock for all items
        for item in sale.items:
            product = Product.objects.get(id=item.product_id)
            if product.stock < item.quantity:
                raise InsufficientStockError(
                    product_id=item.product_id,
                    requested=item.quantity,
                    available=product.stock
                )
        
        # Create the sale
        sale_orm = SaleORM(
            uid=uuid4() if not sale.uid else sale.uid,
            invoice_number=sale.invoice_number,
            total_amount=sale.total_amount,
            payment_method=sale.payment_method,
            point_of_sale_id=sale.point_of_sale_id,
            company_id=sale.company_id,
            user_id=sale.user_id,
            notes=sale.notes
        )
        sale_orm.save()
        
        # Create the items and update stock
        for item in sale.items:
            self._create_item(sale_orm.id, item)
        
        # Refresh the sale to get the items
        sale_orm.refresh_from_db()
        
        return self._to_domain(sale_orm)
    
    @transaction.atomic
    def update(self, sale: Sale) -> Sale:
        """
        Update an existing sale.
        
        Args:
            sale: The sale to update.
            
        Returns:
            The updated sale.
            
        Raises:
            SaleNotFoundError: If the sale is not found.
        """
        try:
            sale_orm = SaleORM.objects.get(id=sale.id)
        except SaleORM.DoesNotExist:
            raise SaleNotFoundError(sale.id)
        
        # Update the sale
        sale_orm.invoice_number = sale.invoice_number
        sale_orm.total_amount = sale.total_amount
        sale_orm.payment_method = sale.payment_method
        sale_orm.point_of_sale_id = sale.point_of_sale_id
        sale_orm.notes = sale.notes
        sale_orm.save()
        
        return self._to_domain(sale_orm)
    
    @transaction.atomic
    def delete(self, sale_id: int) -> None:
        """
        Delete a sale.
        
        Args:
            sale_id: The ID of the sale to delete.
            
        Raises:
            SaleNotFoundError: If the sale is not found.
        """
        try:
            sale_orm = SaleORM.objects.get(id=sale_id)
        except SaleORM.DoesNotExist:
            raise SaleNotFoundError(sale_id)
        
        # Delete the sale
        sale_orm.delete()
    
    @transaction.atomic
    def add_item(self, sale_id: int, item: SaleItem) -> SaleItem:
        """
        Add an item to a sale.
        
        Args:
            sale_id: The ID of the sale.
            item: The item to add.
            
        Returns:
            The added item.
            
        Raises:
            SaleNotFoundError: If the sale is not found.
            InsufficientStockError: If there is insufficient stock for the product.
        """
        try:
            sale_orm = SaleORM.objects.get(id=sale_id)
        except SaleORM.DoesNotExist:
            raise SaleNotFoundError(sale_id)
        
        # Check stock
        product = Product.objects.get(id=item.product_id)
        if product.stock < item.quantity:
            raise InsufficientStockError(
                product_id=item.product_id,
                requested=item.quantity,
                available=product.stock
            )
        
        # Create the item
        item_orm = self._create_item(sale_id, item)
        
        # Update the sale total
        sale_orm.total_amount += item_orm.total_price
        sale_orm.save()
        
        return self._item_to_domain(item_orm)
    
    @transaction.atomic
    def update_item(self, item: SaleItem) -> SaleItem:
        """
        Update a sale item.
        
        Args:
            item: The item to update.
            
        Returns:
            The updated item.
            
        Raises:
            SaleItemNotFoundError: If the item is not found.
            InsufficientStockError: If there is insufficient stock for the product.
        """
        try:
            item_orm = SaleItemORM.objects.get(id=item.id)
        except SaleItemORM.DoesNotExist:
            raise SaleItemNotFoundError(item.id)
        
        # Check stock if quantity is increasing
        if item.quantity > item_orm.quantity:
            product = Product.objects.get(id=item.product_id)
            additional_quantity = item.quantity - item_orm.quantity
            if product.stock < additional_quantity:
                raise InsufficientStockError(
                    product_id=item.product_id,
                    requested=additional_quantity,
                    available=product.stock
                )
            
            # Update stock
            product.stock -= additional_quantity
            product.save()
        elif item.quantity < item_orm.quantity:
            # Return stock if quantity is decreasing
            product = Product.objects.get(id=item.product_id)
            returned_quantity = item_orm.quantity - item.quantity
            product.stock += returned_quantity
            product.save()
        
        # Update the item
        old_total = item_orm.total_price
        
        item_orm.quantity = item.quantity
        item_orm.unit_price = item.unit_price
        item_orm.discount = item.discount
        item_orm.save()  # This will recalculate total_price
        
        # Update the sale total
        sale_orm = item_orm.sale
        sale_orm.total_amount = sale_orm.total_amount - old_total + item_orm.total_price
        sale_orm.save()
        
        return self._item_to_domain(item_orm)
    
    @transaction.atomic
    def delete_item(self, item_id: int) -> None:
        """
        Delete a sale item.
        
        Args:
            item_id: The ID of the item to delete.
            
        Raises:
            SaleItemNotFoundError: If the item is not found.
        """
        try:
            item_orm = SaleItemORM.objects.get(id=item_id)
        except SaleItemORM.DoesNotExist:
            raise SaleItemNotFoundError(item_id)
        
        # Return stock
        product = Product.objects.get(id=item_orm.product_id)
        product.stock += item_orm.quantity
        product.save()
        
        # Update the sale total
        sale_orm = item_orm.sale
        sale_orm.total_amount -= item_orm.total_price
        sale_orm.save()
        
        # Delete the item
        item_orm.delete()
    
    @transaction.atomic
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
        try:
            sale_orm = SaleORM.objects.get(id=sale_id)
        except SaleORM.DoesNotExist:
            raise SaleNotFoundError(sale_id)
        
        if sale_orm.is_cancelled:
            raise SaleAlreadyCancelledError(sale_id)
        
        # Return stock for all items
        for item_orm in sale_orm.sale_items.all():
            product = Product.objects.get(id=item_orm.product_id)
            product.stock += item_orm.quantity
            product.save()
        
        # Mark the sale as cancelled
        sale_orm.is_cancelled = True
        sale_orm.cancelled_at = timezone.now()
        sale_orm.cancelled_by_id = user_id
        sale_orm.save()
        
        return self._to_domain(sale_orm)
    
    def _create_item(self, sale_id: int, item: SaleItem) -> SaleItemORM:
        """
        Create a sale item.
        
        Args:
            sale_id: The ID of the sale.
            item: The item to create.
            
        Returns:
            The created item.
        """
        # Update stock
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
        
        # Create the item
        item_orm = SaleItemORM(
            uid=uuid4() if not item.uid else item.uid,
            sale_id=sale_id,
            product_id=item.product_id,
            product_variant_id=item.product_variant_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount=item.discount
        )
        item_orm.save()
        
        return item_orm
    
    def _to_domain(self, sale_orm: SaleORM) -> Sale:
        """
        Convert an ORM sale to a domain sale.
        
        Args:
            sale_orm: The ORM sale to convert.
            
        Returns:
            The domain sale.
        """
        items = [self._item_to_domain(item_orm) for item_orm in sale_orm.sale_items.all()]
        
        return Sale(
            id=sale_orm.id,
            uid=sale_orm.uid,
            invoice_number=sale_orm.invoice_number,
            date=sale_orm.date,
            total_amount=sale_orm.total_amount,
            payment_method=sale_orm.payment_method,
            items=items,
            point_of_sale_id=sale_orm.point_of_sale_id,
            company_id=sale_orm.company_id,
            user_id=sale_orm.user_id,
            is_cancelled=sale_orm.is_cancelled,
            cancelled_at=sale_orm.cancelled_at,
            cancelled_by_id=sale_orm.cancelled_by_id,
            notes=sale_orm.notes,
            is_active=sale_orm.is_active
        )
    
    def _item_to_domain(self, item_orm: SaleItemORM) -> SaleItem:
        """
        Convert an ORM sale item to a domain sale item.
        
        Args:
            item_orm: The ORM sale item to convert.
            
        Returns:
            The domain sale item.
        """
        return SaleItem(
            id=item_orm.id,
            uid=item_orm.uid,
            sale_id=item_orm.sale_id,
            product_id=item_orm.product_id,
            product_variant_id=item_orm.product_variant_id,
            quantity=item_orm.quantity,
            unit_price=item_orm.unit_price,
            discount=item_orm.discount,
            total_price=item_orm.total_price,
            is_active=item_orm.is_active
        )

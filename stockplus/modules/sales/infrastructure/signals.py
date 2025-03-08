"""
Signals for the sales module.
"""

import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from stockplus.modules.product.infrastructure.models import Product
from stockplus.modules.sales.infrastructure.models import Sale, SaleItem
from stockplus.modules.sales.infrastructure.utils import generate_invoice_number

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Sale)
def generate_invoice_number_for_sale(sender, instance, **kwargs):
    """
    Generate an invoice number for a new sale.
    
    Args:
        sender: The model class.
        instance: The actual instance being saved.
        **kwargs: Additional keyword arguments.
    """
    if not instance.invoice_number:
        try:
            # Generate a unique invoice number
            instance.invoice_number = generate_invoice_number(instance.company_id)
            logger.info(f"Generated invoice number {instance.invoice_number} for sale")
        except Exception as e:
            logger.error(f"Failed to generate invoice number for sale: {e}")


@receiver(post_save, sender=SaleItem)
def update_product_stock(sender, instance, created, **kwargs):
    """
    Update product stock when a sale item is created.
    
    Args:
        sender: The model class.
        instance: The actual instance being saved.
        created: A boolean; True if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created and not instance.sale.is_cancelled:
        try:
            # Update product stock
            product = Product.objects.get(id=instance.product_id)
            product.stock -= instance.quantity
            product.save(update_fields=['stock'])
            
            logger.info(f"Updated stock for product {product.name} to {product.stock}")
            
            # Check if stock is low
            if product.is_low_stock:
                logger.warning(f"Low stock alert for product {product.name}: {product.stock} items remaining (threshold: {product.low_stock_threshold})")
        except Exception as e:
            logger.error(f"Failed to update product stock: {e}")


@receiver(post_save, sender=Sale)
def handle_sale_cancellation(sender, instance, **kwargs):
    """
    Handle sale cancellation.
    
    Args:
        sender: The model class.
        instance: The actual instance being saved.
        **kwargs: Additional keyword arguments.
    """
    if instance.is_cancelled:
        try:
            # Return stock for all items
            for item in instance.sale_items.all():
                product = Product.objects.get(id=item.product_id)
                product.stock += item.quantity
                product.save(update_fields=['stock'])
                
                logger.info(f"Returned stock for product {product.name} to {product.stock} after sale cancellation")
        except Exception as e:
            logger.error(f"Failed to handle sale cancellation: {e}")

"""
Signals for the product module.
"""

import io
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from barcode import EAN13
from barcode.writer import ImageWriter

from stockplus.modules.product.infrastructure.models import Product
from stockplus.modules.product.infrastructure.utils import generate_ean13_barcode

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Product)
def generate_product_barcode(sender, instance, created, **kwargs):
    """
    Generate a barcode for a new product.
    
    Args:
        sender: The model class.
        instance: The actual instance being saved.
        created: A boolean; True if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created and not instance.barcode:
        try:
            # Generate a unique EAN-13 barcode
            barcode = generate_ean13_barcode(instance.company_id)
            
            # Update the product with the barcode
            instance.barcode = barcode
            
            # Generate barcode image
            barcode_image = io.BytesIO()
            EAN13(barcode, writer=ImageWriter()).write(barcode_image)
            instance.barcode_image.save(f"{barcode}.png", ContentFile(barcode_image.getvalue()), save=False)
            
            instance.save(update_fields=['barcode', 'barcode_image'])
            
            logger.info(f"Generated barcode {barcode} and image for product {instance.name}")
        except Exception as e:
            logger.error(f"Failed to generate barcode for product {instance.name}: {e}")


@receiver(post_save, sender=Product)
def check_low_stock(sender, instance, **kwargs):
    """
    Check if a product has low stock and send a notification if needed.
    
    Args:
        sender: The model class.
        instance: The actual instance being saved.
        **kwargs: Additional keyword arguments.
    """
    if instance.is_low_stock:
        # Here we would send a notification to the user
        # For now, we'll just log it
        logger.warning(f"Low stock alert for product {instance.name}: {instance.stock} items remaining (threshold: {instance.low_stock_threshold})")

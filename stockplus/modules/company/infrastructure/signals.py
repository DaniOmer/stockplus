"""
Registration signals for the company application.
This module contains signals that are triggered when a company is created.
"""

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from stockplus.modules.company.infrastructure.models import Company
from stockplus.modules.pointofsale.domain.entities import PointOfSale as PointOfSaleEntity
from stockplus.modules.pointofsale.infrastructure.repositories.pos_repository import PointOfSaleRepository

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Company)
def create_default_pos_for_new_company(sender, instance, created, **kwargs):
    """
    Create a default Point of Sale for a new company.
    """
    if created:
        try:
            # Create a default Point of Sale
            pos_repository = PointOfSaleRepository()
            pos_entity = PointOfSaleEntity(
                name="Default Point of Sale",
                type="store",
                company_id=instance.id,
                collaborator_ids=[instance.id],
                is_active=True,
                is_default=True
            )
            pos_repository.create(pos_entity)
            
            logger.info(f"Successfully created default Point of Sale for company {instance.denomination}")
        except Exception as e:
            logger.error(f"Failed to create default Point of Sale for company: {e}")
"""
Registration signals for the user application.
This module contains signals that are triggered when a user registers.
"""

import logging
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from stockplus.modules.company.domain.entities.company_entity import Company as CompanyEntity
from stockplus.modules.company.infrastructure.repositories.company_repository import CompanyRepository
from stockplus.modules.pointofsale.domain.entities import PointOfSale as PointOfSaleEntity
from stockplus.modules.pointofsale.infrastructure.repositories.pos_repository import PointOfSaleRepository
from stockplus.modules.subscription.models import Subscription, SubscriptionPlan

logger = logging.getLogger(__name__)

User = get_user_model()

@receiver(post_save, sender=User)
def create_company_and_pos_for_new_user(sender, instance, created, **kwargs):
    """
    Create a company and a default Point of Sale for a new user.
    """
    if created:
        try:
            # Create a company for the user
            company_repository = CompanyRepository()
            company_entity = CompanyEntity(
                denomination=f"{instance.first_name}'s Company",
                legal_form="Individual",
                is_active=True
            )
            company = company_repository.save(company_entity)
            
            # Assign the user to the company
            instance.company_id = company.id
            instance.role = "owner"
            instance.save()
            
            # Create a default Point of Sale
            pos_repository = PointOfSaleRepository()
            pos_entity = PointOfSaleEntity(
                name="Default Point of Sale",
                type="store",
                company_id=company.id,
                collaborator_ids=[instance.id],
                is_active=True
            )
            pos_repository.create(pos_entity)
            
            logger.info(f"Successfully created company and default Point of Sale for user {instance.email}")
        except Exception as e:
            logger.error(f"Failed to create company and Point of Sale for user {instance.email}: {e}")

@receiver(post_save, sender=User)
def create_free_trial_subscription(sender, instance, created, **kwargs):
    """
    Create a 30-day free trial subscription for a new user.
    """
    if created and instance.company_id:
        try:
            # Get the default subscription plan
            default_plan = SubscriptionPlan.objects.filter(active=True).first()
            
            if default_plan:
                # Create a subscription
                start_date = datetime.now()
                end_date = start_date + timedelta(days=30)
                
                subscription = Subscription.objects.create(
                    user=instance,
                    company_id=instance.company_id,
                    subscription_plan=default_plan,
                    interval='month',
                    start_date=start_date,
                    end_date=end_date,
                    renewal_date=end_date,
                    status='active'
                )
                
                # Add user to the subscription plan's group
                if default_plan.group:
                    instance.groups.add(default_plan.group)
                
                logger.info(f"Successfully created 30-day free trial subscription for user {instance.email}")
            else:
                logger.warning(f"No active subscription plan found for user {instance.email}")
        except Exception as e:
            logger.error(f"Failed to create subscription for user {instance.email}: {e}")

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
from stockplus.modules.address.infrastructure.models import CompanyAddress, UserAddress

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
                is_active=True,
                is_default=True
            )
            pos_repository.create(pos_entity)
            
            logger.info(f"Successfully created company and default Point of Sale for user {instance.email}")
        except Exception as e:
            logger.error(f"Failed to create company and Point of Sale for user {instance.email}: {e}")

@receiver(post_save, sender=UserAddress)
def create_company_address_from_user_address(sender, instance, created, **kwargs):
    """
    Create a company address from the user's address.
    """
    if created and instance.user and instance.user.company_id:
        try:
            # Check if the company already has an address
            if not CompanyAddress.objects.filter(company_id=instance.user.company_id).exists():
                # Create a company address based on the user's address
                CompanyAddress.objects.create(
                    company_id=instance.user.company_id,
                    address=instance.address,
                    complement=instance.complement,
                    city=instance.city,
                    postal_code=instance.postal_code,
                    state=instance.state,
                    country=instance.country,
                    country_code=instance.country_code
                )
                
                logger.info(f"Successfully created company address for company {instance.user.company_id}")
        except Exception as e:
            logger.error(f"Failed to create company address: {e}")


@receiver(post_save, sender=User)
def create_free_trial_subscription(sender, instance, created, **kwargs):
    """
    Create a free trial subscription for a new user.
    """
    if created and instance.company_id:
        try:
            # Get the free trial subscription plan
            free_trial_plan = SubscriptionPlan.objects.filter(is_free_trial=True, active=True).first()
            
            # If no free trial plan exists, fall back to any active plan
            if not free_trial_plan:
                free_trial_plan = SubscriptionPlan.objects.filter(active=True).first()
                trial_days = 30  # Default to 30 days if no free trial plan
            else:
                trial_days = free_trial_plan.trial_days
            
            if free_trial_plan:
                # Create a subscription
                start_date = datetime.now()
                end_date = start_date + timedelta(days=trial_days)
                
                subscription = Subscription.objects.create(
                    user=instance,
                    company_id=instance.company_id,
                    subscription_plan=free_trial_plan,
                    interval='month',
                    start_date=start_date,
                    end_date=end_date,
                    renewal_date=end_date,
                    status='active'
                )
                
                # Add user to the subscription plan's group
                if free_trial_plan.group:
                    instance.groups.add(free_trial_plan.group)
                
                logger.info(f"Successfully created {trial_days}-day free trial subscription for user {instance.email}")
            else:
                logger.warning(f"No active subscription plan found for user {instance.email}")
        except Exception as e:
            logger.error(f"Failed to create subscription for user {instance.email}: {e}")

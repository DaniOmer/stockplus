"""
Notification signals for the user application.
This module contains signals that are triggered for user notifications.
"""

import logging
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from stockplus.modules.shop.infrastructure.models import Customer
from stockplus.modules.shop.services import CustomerService
from stockplus.modules.user.infrastructure.models import Invitation
from stockplus.modules.messenger.infrastructure.utils import send_mail_message
from stockplus.modules.user.infrastructure.utils import get_verification_data_missive, get_invitation_data_missive
from stockplus.modules.user.application.services import InvitationService
from stockplus.modules.user.infrastructure.repositories import InvitationRepository


logger = logging.getLogger(__name__)

User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    """
    Send an activation email when a user is created.
    """
    if created:
        try:
            # Don't send activation email if the user was created from an invitation
            invitation_service = InvitationService(InvitationRepository())
            existing_invitation = invitation_service.get_invitation_by_email(instance.email)
            if not existing_invitation:
                data = get_verification_data_missive(instance)
                if data:
                    send_mail_message(**data)
                    logger.info(f"Activation email successfully sent to {instance.email}")
        except Exception as e:
            logger.error(f"Failed to send activation email: {e}")

@receiver(post_save, sender=User)
def create_customer_for_verified_user(sender, instance, created, **kwargs):
    """
    Create a Stripe customer when a user is verified.
    """
    # Check if the user is verified and doesn't already have a customer
    customer_exists = Customer.objects.filter(user=instance).exists()
    if instance.is_verified and not customer_exists:
        try:
            # Create a customer
            customer, created = Customer.objects.get_or_create(user=instance)
                
            # Generate a Stripe ID if it doesn't exist
            if created or not customer.stripe_id:
                # Get the user's full name
                full_name = f"{instance.first_name} {instance.last_name}".strip()
                if not full_name:
                    full_name = instance.email or instance.phone_number or "Customer"
                    
                # Create a Stripe customer
                stripe_id = CustomerService.create_stripe_customer(
                    name=full_name,
                    email=instance.email,
                    metadata={'user_id': instance.id}
                )
                    
                # Update the customer with the Stripe ID
                if stripe_id:
                    customer.stripe_id = stripe_id
                    customer.save()
                    logger.info(f"Successfully created a Stripe customer for {instance.email}")
                else:
                    logger.error(f"Failed to create a Stripe customer for {instance.email}")
        except Exception as e:
            logger.error(f"Error creating customer for {instance.email}: {str(e)}")

@receiver(post_save, sender=Invitation)
def send_invitation_mail(sender, instance, created, **kwargs):
    """
    Send an invitation email when an invitation is created.
    """
    if created:
        try:
            data = get_invitation_data_missive(instance)
            if data:
                send_mail_message(
                    subject=f"{instance.sender.first_name} vous invite à rejoindre Stockplus",
                    target=instance.email,
                    template='invitation_mail.html',
                    html=data.html,
                    message=data.txt
                )
                logger.info(f"Invitation email successfully sent to {instance.email}")
        except Exception as e:
            logger.error(f"Failed to send invitation email: {e}")

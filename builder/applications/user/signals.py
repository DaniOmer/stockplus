from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from builder.models import Customer, Invitation, Missive
from builder.applications.user.utils import get_verification_data_missive, get_invitation_data_missive

import logging
logger = logging.getLogger(__name__)

User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        try:
            if not Invitation.objects.filter(email=instance.email).exists():
                data = get_verification_data_missive(instance)
                missive = Missive(**data)
                missive.save()
                logger.info(f"Activation email successfully sent to {instance.email}")

        except Exception as e:
            logger.error(f"Failed to send activation email : {e}.")

@receiver(post_save, sender=User)
def create_customer_for_verifed_user(sender, instance, created, **kwargs):
    if 'builder.applications.shop' in settings.INSTALLED_APPS:
        qs = Customer.objects.filter(user=instance).exists()
        if instance.is_verified and not qs:
            try:
                customer, created = Customer.objects.get_or_create(user=instance)
                if created:
                    logger.info(f"Successfully created a customer for {instance.email}.")
            except Exception as e:
                logger.error(f"Error creating customer for {instance.email}: {str(e)}")

@receiver(post_save, sender=Invitation)
def send_invitation_mail(sender, instance, created, **kwargs):
    if created:
        try:
            data = get_invitation_data_missive(instance)
            missive = Missive(**data)
            missive.save()
            logger.info(f"Invitation email successfully sent to {instance.email}.")

        except Exception as e:
            logger.error(f"Failed to send invitation email : {e}.")
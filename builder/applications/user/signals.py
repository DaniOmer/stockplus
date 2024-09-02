from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from builder.models import Missive
from builder.applications.user.utils import get_verification_data_missive

import logging
logger = logging.getLogger(__name__)

User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        try:
            data = get_verification_data_missive(instance)
            missive = Missive(**data)
            missive.save()
            logger.info(f"Activation email successfully sent to {instance.email}")

        except Exception as e:
            logger.error(f"Failed to send activation email : {e}.")

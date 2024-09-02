from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from builder.applications.user.utils import generate_verification_url
from builder.models import Missive

import logging
logger = logging.getLogger(__name__)

User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        try:
            data = get_data_missive(instance)
            missive = Missive(**data)
            missive.save()
            logger.info(f"Activation email successfully sent to {instance.email}")

        except Exception as e:
            logger.error(f"Failed to send activation email : {e}.")


def get_data_missive(user):
    verification_url = generate_verification_url(user)
    if verification_url is not None:
        html_content = render_to_string('activation_mail.html', {'user': user, 'verification_url': str(verification_url)})
        return {
            "content_type": None,
            "object_id": None,
            "subject": 'Bienvenue chez Stockplus',
            "html": html_content,
            "txt": html_content,
            "target": user.email,
            "mode": 'EMAIL',
            "template": 'activation_mail.html'
        }
    return None
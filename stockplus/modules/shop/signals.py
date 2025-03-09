from django.db.models.signals import post_save
from django.dispatch import receiver

from stockplus.modules.shop.infrastructure.models import Customer

@receiver(post_save, sender=Customer)
def create_stripe_customer(sender, instance, created, **kwargs):
    if created and not instance.stripe_id:
        stripe_id = instance.get_stripe_id()
        instance.stripe_id = stripe_id
        instance.save()
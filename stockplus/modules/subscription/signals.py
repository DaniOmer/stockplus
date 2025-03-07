import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)
from stockplus.modules.subscription.models import SubscriptionPlan, SubscriptionPricing


@receiver(post_save, sender=SubscriptionPlan)
def create_stripe_product(sender, instance, created, **kwargs):
    """Create stripe product for a given subscription plan."""
    if created and not instance.stripe_id:
        stripe_id = instance.get_stripe_id()
        instance.stripe_id = stripe_id
        instance.save()

@receiver(post_save, sender=SubscriptionPricing)
def creat_stripe_price(sender, instance, created, **kwargs):
    """ Create stripe price for each new created subscription plan pricing. """
    if created and not instance.stripe_id:
        stripe_id = instance.get_stripe_id()
        instance.stripe_id = stripe_id
        instance.save()

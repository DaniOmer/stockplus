import logging
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from builder.models.base import Base
from builder.applications.shop.services import CustomerService

User = get_user_model()
logger = logging.getLogger(__name__)

class Customer(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        abstract = True
    
    def get_stripe_id(self):
        if self.user.is_verified:
            try:
                stripe_id = CustomerService.create_stripe_customer(
                    name=self.user.fullname,
                    email=self.user.email,
                    metadata={'user_id': self.user.id}
                )
                return stripe_id
            except Exception as e:
                logger.info(f"Failed to create stripe Customer for user {self.user.name} : {e}")
                return None
        return None
    
@receiver(post_save, sender=Customer)
def create_stripe_customer(sender, instance, created, **kwargs):
    if created and not instance.stripe_id:
        stripe_id = instance.get_stripe_id()
        instance.stripe_id = stripe_id
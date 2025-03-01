import logging
from django.db import models
from django.contrib.auth import get_user_model

from builder.models.base import Base
from builder.modules.shop.services import CustomerService

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
                logger.info(f"Failed to create stripe Customer for user {self.user.fullname} : {e}")
                return None
        return None
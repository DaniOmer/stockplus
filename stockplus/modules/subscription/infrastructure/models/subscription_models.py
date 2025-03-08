import logging
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from datetime import timezone
from dateutil.relativedelta import relativedelta

from stockplus.models.base import Base
from stockplus.modules.subscription import choices
from stockplus.modules.shop.services import ProductService, PriceService
from stockplus.modules.company.infrastructure.models import Company

logger = logging.getLogger(__name__)

User = get_user_model()


class Feature(Base):
    """
    ORM model for a subscription feature.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'stockplus_feature'
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'

    def __str__(self):
        return f"{self.name}"


class SubscriptionPlan(Base):
    """
    ORM model for a subscription plan.
    SUBSCRIPTION PLAN is equivalent to STRIPE PRODUCT
    """
    if settings.SUBSCRIPTION_MODEL if hasattr(settings, 'SUBSCRIPTION_MODEL') else False:
        name = models.CharField(max_length=255, choices=settings.SUBSCRIPTION_MODEL, unique=True)
    else:
        name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    features = models.ManyToManyField(Feature, related_name='features')
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(
        Permission, 
        related_name='permissions', 
        limit_choices_to={
            "content_type__app_label": "stockplus",
            "codename__in": [x[0] for x in settings.SUBSCRIPTION_PERMISSIONS] if hasattr(settings, 'SUBSCRIPTION_PERMISSIONS') else []
        }
    )
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    pos_limit = models.IntegerField(default=3, help_text="Maximum number of points of sale allowed for this plan. 0 means unlimited.")
    is_free_trial = models.BooleanField(default=False, help_text="Indicates if this plan is for free trials.")
    trial_days = models.IntegerField(default=30, help_text="Number of days for the free trial period.")
    
    class Meta:
        db_table = 'stockplus_subscriptionplan'
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'
        permissions = settings.SUBSCRIPTION_PERMISSIONS if hasattr(settings, 'SUBSCRIPTION_PERMISSIONS') else []
    
    def __str__(self):
        return f"{self.name}"
    
    def get_stripe_id(self):
        """
        Get or create a Stripe product ID for this subscription plan.
        
        Returns:
            The Stripe product ID.
        """
        try:
            stripe_id = ProductService.create_stripe_product(
                name=self.name,
                description=self.description if self.description else self.name,
                active=self.active,
                metadata={ 'subscription_plan_id': self.id }
            )
            return stripe_id
        except Exception as e:
            logger.error(f"An error occurred while creating stripe product for {self.name}: {e}")
            return None


class SubscriptionPricing(Base):
    """
    ORM model for subscription pricing.
    SUBSCRIPTION PRICING is equivalent to STRIPE PRICE
    """
    subscription_plan = models.ForeignKey(SubscriptionPlan, related_name='pricing', on_delete=models.SET_NULL, null=True)
    interval = models.CharField(max_length=100, choices=choices.SUBSCRIPTION_INTERVAL, default='month')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=choices.CURRENCY, default='eur')
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        db_table = 'stockplus_subscriptionpricing'
        verbose_name = 'Subscription Pricing'
        verbose_name_plural = 'Subscription Pricings'

    @property
    def stripe_product_id(self):
        """ Get stripe product id related to the subscription plan """
        if self.subscription_plan is None:
            return None
        return self.subscription_plan.stripe_id
    
    @property
    def stripe_price(self):
        """ Remove the price decimal """
        return int(self.price * 100)
    
    @property
    def stripe_interval(self):
        """ 
            Get the interval count based on subscription 
            pricing interval to match Stripe interval. Only
            'day', 'month', 'week' and 'year' are supported
            by Stripe.
        """
        if self.interval not in ['day', 'month', 'week', 'year']:
            return 'month'
        else:
            return self.interval

    @property
    def stripe_interval_count(self):
        """ Get the interval count based on subscription pricing interval """
        if self.interval == 'month':
            return 1
        elif self.interval == 'semester':
            return 6
        elif self.interval == 'year':
            return 1
    
    def __str__(self):
        return f"{self.subscription_plan.name} - {self.interval}: {self.price} {self.currency}"
    
    def get_stripe_id(self):
        """
        Get or create a Stripe price ID for this subscription pricing.
        
        Returns:
            The Stripe price ID.
        """
        try:
            stripe_id = PriceService.create_stripe_price(
                currency=self.currency,
                unit_amount=self.stripe_price, 
                interval=self.stripe_interval, 
                interval_count=self.stripe_interval_count, 
                product=self.stripe_product_id, 
                metadata={"subscription_plan_id": self.subscription_plan.id},
            )
            return stripe_id
        except Exception as e:
            logger.error(f"An error occurred while creating stripe price for {self.subscription_plan.name}: {e}")

    def save(self, *args, **kwags):
        super().save(*args, **kwags)
        """
        Logic to disable existing pricing if the new one is 
        created with the same subscription plan and same interval.
        """
        # Import here to avoid circular imports
        from stockplus.modules.subscription.infrastructure.models.subscription_models import SubscriptionPricing
        if not self.is_disable:
            qs = SubscriptionPricing.objects.filter(
                subscription_plan=self.subscription_plan,
                interval=self.interval,
                currency=self.currency
            ).exclude(id=self.id)
            qs.update(is_disable=True)


class Subscription(Base):
    """
    ORM model for a user subscription.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    if 'stockplus.modules.company' in settings.INSTALLED_APPS:
        company = models.OneToOneField(Company, on_delete=models.CASCADE)

    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    interval = models.CharField(max_length=100, choices=choices.SUBSCRIPTION_INTERVAL, default='month')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    renewal_date = models.DateTimeField()
    status = models.CharField(max_length=100, choices=choices.SUBSCRIPTION_STATUS, default='pending')

    class Meta:
        db_table ='stockplus_subscription'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
    
    def __str__(self):
        return f"Subscription for {self.user} : {self.subscription_plan}"

import logging
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from datetime import timezone
from dateutil.relativedelta import relativedelta

from stockplus.utils import setting
from stockplus.models.base import Base
from stockplus.modules.subscription import choices
from stockplus.modules.subscription import utils
from stockplus.modules.shop.services import ProductService, PriceService
from stockplus.modules.company.infrastructure.models import Company

logger = logging.getLogger(__name__)

User = get_user_model()

class Feature(Base):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class SubscriptionPlan(Base):
    """
    SUBSCRIPTION PLAN is equivalent to STRIPE PRODUCT
    """
    if setting('SUBSCRIPTION_MODEL', False):
        name = models.CharField(max_length=255, choices=settings.SUBSCRIPTION_MODEL, unique=True)
    else:
        name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    features = models.ManyToManyField(Feature, related_name='features')
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, related_name='permissions', 
                                        limit_choices_to={
                                            "content_type__app_label": "stockplus",
                                            "codename__in": [x[0] for x in settings.SUBSCRIPTION_PERMISSIONS]
                                        })
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    class Meta:
        db_table = 'stockplus_subscriptionplan'
        permissions = settings.SUBSCRIPTION_PERMISSIONS
    
    def __str__(self):
        return f"{self.name}"
    
    def get_stripe_id(self):
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
    SUBSCRIPTION PRICING is equivalent to STRIPE PRICE
    """
    subscription_plan = models.ForeignKey(SubscriptionPlan, related_name='pricing', on_delete=models.SET_NULL, null=True)
    interval = models.CharField(max_length=100, choices=choices.SUBSCRIPTION_INTERVAL, default='month')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=choices.CURRENCY, default='eur')
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        db_table = 'stockplus_subscriptionpricing'

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
        # Import ici pour éviter les imports circulaires
        from stockplus.modules.subscription.models import SubscriptionPricing
        if not self.is_disable:
            qs = SubscriptionPricing.objects.filter(
                subscription_plan=self.subscription_plan,
                interval=self.interval,
                currency=self.currency
            ).exclude(id=self.id)
            qs.update(is_disable=True)


class Subscription(Base):
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
    
    def __str__(self):
        return f"Subscription for {self.user} : {self.subscription_plan}"
    
    def pre_activate(self):
        self.start_date = timezone.now()
        if self.interval == 'month':
            self.end_date = self.start_date + relativedelta(months=1)
        elif self.interval == 'semester':
            self.end_date = self.start_date + relativedelta(months=6)
        elif self.interval == 'year':
            self.end_date = self.start_date + relativedelta(years=1)
        
        self.renewal_date = self.end_date

    def activate(self):
        if self.status == 'pending':
            self.status = 'active'
            self.save()
            utils.add_users_to_subscription_group(self)
        else:
            raise ValueError("Cannot activate a subscription that is not in pending state.")

    def expire(self):
        self.status = 'expired'
        self.save()
        utils.remove_users_from_subscription_group(self)
    
    def cancel(self):
        self.status = 'cancelled'
        self.save()

    def get_price(self):
        # Import ici pour éviter les imports circulaires
        from stockplus.modules.subscription.models import SubscriptionPricing as Pricing
        pricing = Pricing.objects.filter(
            subscription_plan=self.subscription_plan,
            interval=self.interval
        ).first()

        if pricing:
            return pricing.price
        return None

from typing import Iterable
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from datetime import timezone
from dateutil.relativedelta import relativedelta

from builder.utils import setting
from builder.models.base import Base
from builder.applications.subscription import choices
from builder.applications.subscription.apps import SubscriptionConfig as conf
from builder.applications.subscription import utils

class Feature(Base):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}"


class SubscriptionPlan(Base):
    """
    SUBSCRIPTION PLAN is equivalent to STRIPE PRODUCT
    """
    if setting('SUBSCRIPTION_MODEL', False):
        name = models.CharField(max_length=255, choices=settings.SUBSCRIPTION_MODEL)
    else:
        name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    features = models.ManyToManyField(conf.ForeignKey.feature, related_name='features')
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, related_name='permissions', 
                                        limit_choices_to={
                                            "content_type__app_label": "builder",
                                            "codename__in": [x[0] for x in settings.SUBSCRIPTION_PERMISSIONS]
                                        })
    class Meta:
        abstract = True
        permissions = settings.SUBSCRIPTION_PERMISSIONS
    
    def __str__(self):
        return f"{self.name}"
    

class SubscriptionPricing(Base):
    """
    SUBSCRIPTION PRICING is equivalent to STRIPE PRICE
    """
    subscription_plan = models.ForeignKey(conf.ForeignKey.subscription_plan, related_name='pricing', on_delete=models.SET_NULL, null=True)
    interval = models.CharField(max_length=100, choices=choices.SUBSCRIPTION_INTERVAL, default='month')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=choices.CURRENCY, default='euro')

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.subscription_plan.name} - {self.interval}: {self.price} {self.currency}"

    def save(self, *args, **kwags):
        super().save(*args, **kwags)
        from builder.models import SubscriptionPricing
        if not self.is_disable:
            qs = SubscriptionPricing.objects.filter(
                subscription_plan=self.subscription_plan,
                interval=self.interval
            ).exclude(id=self.id)
            qs.update(is_disable=True)


class Subscription(Base):
    user = models.OneToOneField(conf.ForeignKey.user, on_delete=models.CASCADE)
    if 'builder.applications.company' in settings.INSTALLED_APPS:
        company = models.OneToOneField(conf.ForeignKey.company, on_delete=models.CASCADE)

    subscription_plan = models.ForeignKey(conf.ForeignKey.subscription_plan, on_delete=models.SET_NULL, null=True, blank=True)
    interval = models.CharField(max_length=100, choices=choices.SUBSCRIPTION_INTERVAL, default='month')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    renewal_date = models.DateTimeField()
    status = models.CharField(max_length=100, choices=choices.SUBSCRIPTION_STATUS, default='pending')

    class Meta:
        abstract = True
    
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
        from builder.models import SubscriptionPricing as Pricing
        pricing = Pricing.objects.filter(
            subscription_plan=self.subscription_plan,
            interval=self.interval
        ).first()

        if pricing:
            return pricing.price
        return None
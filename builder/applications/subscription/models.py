from django.db import models
from django.conf import settings

from builder.functions import setting
from builder.models.base import Base
from builder.applications.subscription import choices
from builder.applications.subscription.apps import SubscriptionConfig as conf

class Feature(Base):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SubscriptionPlan(Base):
    if setting('SUBSCRIPTION_MODEL', False):
        name = models.CharField(max_length=255, choices=settings.SUBSCRIPTION_MODEL)
    else:
        name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)
    features = models.ManyToManyField(conf.ForeignKey.feature, blank=True, null=True, related_name='features')

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name


class Subscription(Base):
    subscription_plan = models.ForeignKey(conf.ForeignKey.subscription_plan)
    if 'builder.applications.company' in settings.INSTALLED_APPS and settings.SAAS_MODEL == 'B2B':
        company = models.ForeignKey(conf.ForeignKey.company)
    else: 
        user = models.ForeignKey(conf.ForeignKey.user)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    renewal_date = models.DateTimeField()
    status = models.CharField(max_length=100, choices=choices.SUBSCRIPTION_STATUS)

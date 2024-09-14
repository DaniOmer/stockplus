from django.contrib import admin
from django.conf import settings

from builder import models as all_models

if 'builder.applications.subscription' in settings.INSTALLED_APPS:
    from builder.applications.subscription import admin as admin_subscription
    @admin.register(all_models.Feature)
    class FeatureAdmin(admin_subscription.FeatureAdmin): pass

    @admin.register(all_models.SubscriptionPlan)
    class SubscriptionAdmin(admin_subscription.SubscriptionPlanAdmin): pass

    @admin.register(all_models.Subscription)
    class SubscriptionAdmin(admin_subscription.SubscriptionAdmin): pass
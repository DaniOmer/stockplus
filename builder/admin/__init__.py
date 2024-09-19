from django.contrib import admin
from django.conf import settings

from builder import models as all_models

if 'builder.applications.user' in settings.INSTALLED_APPS:
    from builder.applications.user import admin as admin_user
    @admin.register(all_models.User)
    class UserAdmin(admin_user.UserAdmin): pass

if 'builder.applications.company' in settings.INSTALLED_APPS:
    from builder.applications.company import admin as admin_company
    @admin.register(all_models.Company)
    class CompanyAdmin(admin_company.CompanyAdmin): pass

if 'builder.applications.messenger' in settings.INSTALLED_APPS:
    from builder.applications.messenger import admin as admin_messenger
    @admin.register(all_models.Missive)
    class MissiveAdmin(admin_messenger.MissiveAdmin): pass

if 'builder.applications.subscription' in settings.INSTALLED_APPS:
    from builder.applications.subscription import admin as admin_subscription
    @admin.register(all_models.Feature)
    class FeatureAdmin(admin_subscription.FeatureAdmin): pass

    @admin.register(all_models.SubscriptionPlan)
    class SubscriptionPlanAdmin(admin_subscription.SubscriptionPlanAdmin): pass

    @admin.register(all_models.SubscriptionPricing)
    class SubscriptionPricingAdmin(admin_subscription.SubscriptionPricingAdmin): pass

    @admin.register(all_models.Subscription)
    class SubscriptionAdmin(admin_subscription.SubscriptionAdmin): pass
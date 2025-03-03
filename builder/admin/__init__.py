from django.contrib import admin
from django.conf import settings

from builder import models as all_models

if 'builder.modules.user' in settings.INSTALLED_APPS:
    from builder.modules.user import admin as admin_user
    @admin.register(all_models.User)
    class UserAdmin(admin_user.UserAdmin): pass

if 'builder.modules.company' in settings.INSTALLED_APPS:
    from builder.modules.company import admin as admin_company
    # Skip registering Company model since it's abstract
    # @admin.register(all_models.Company)
    # class CompanyAdmin(admin_company.CompanyAdmin): pass

if 'builder.modules.messenger' in settings.INSTALLED_APPS:
    from builder.modules.messenger import admin as admin_messenger
    # Skip registering Missive model since it's abstract
    # @admin.register(all_models.Missive)
    # class MissiveAdmin(admin_messenger.MissiveAdmin): pass

if 'builder.modules.subscription' in settings.INSTALLED_APPS:
    from builder.modules.subscription import admin as admin_subscription
    # Skip registering Feature model since it's abstract
    # @admin.register(all_models.Feature)
    # class FeatureAdmin(admin_subscription.FeatureAdmin): pass

    # Skip registering SubscriptionPlan model since it's abstract
    # @admin.register(all_models.SubscriptionPlan)
    # class SubscriptionPlanAdmin(admin_subscription.SubscriptionPlanAdmin): pass

    # Skip registering Subscription model since it's abstract
    # @admin.register(all_models.Subscription)
    # class SubscriptionAdmin(admin_subscription.SubscriptionAdmin): pass

if 'builder.modules.shop' in settings.INSTALLED_APPS:
    from builder.modules.shop import admin as admin_shop
    # Skip registering Customer model since it's abstract
    # @admin.register(all_models.Customer)
    # class CustomerAdmin(admin_shop.CustomerAdmin): pass

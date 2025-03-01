from django.conf import settings

if 'builder.modules.messenger' in settings.INSTALLED_APPS:
    from builder.modules.messenger import models as models_messenger
    class Missive(models_messenger.Missive): pass

if 'builder.modules.user' in settings.INSTALLED_APPS:
    from builder.modules.user import models as models_user
    class User(models_user.User): pass
    class UserAddress(models_user.UserAddress): pass
    class Invitation(models_user.Invitation): pass

if 'builder.modules.company' in settings.INSTALLED_APPS:
    from builder.modules.company import models as models_company
    class Company(models_company.Company): pass
    class CompanyAddress(models_company.CompanyAddress): pass

if 'builder.modules.subscription' in settings.INSTALLED_APPS:
    from builder.modules.subscription import models as models_subscription
    class Feature(models_subscription.Feature): pass
    class SubscriptionPlan(models_subscription.SubscriptionPlan): pass
    class SubscriptionPricing(models_subscription.SubscriptionPricing): pass
    class Subscription(models_subscription.Subscription): pass

if 'builder.modules.shop' in settings.INSTALLED_APPS:
    from builder.modules.shop import models as models_shop
    class Customer(models_shop.Customer): pass
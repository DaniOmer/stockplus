from django.conf import settings

if 'builder.applications.messenger' in settings.INSTALLED_APPS:
    from builder.applications.messenger import models as models_messenger
    class Missive(models_messenger.Missive): pass

if 'builder.applications.user' in settings.INSTALLED_APPS:
    from builder.applications.user import models as models_user
    class User(models_user.User): pass
    class UserAddress(models_user.UserAddress): pass
    class Invitation(models_user.Invitation): pass

if 'builder.applications.company' in settings.INSTALLED_APPS:
    from builder.applications.company import models as models_company
    class Company(models_company.Company): pass
    class CompanyAddress(models_company.CompanyAddress): pass

if 'builder.applications.subscription' in settings.INSTALLED_APPS:
    from builder.applications.subscription import models as models_subscription
    class Feature(models_subscription.Feature): pass
    class SubscriptionPlan(models_subscription.SubscriptionPlan): pass
    class SubscriptionPricing(models_subscription.SubscriptionPricing): pass
    class Subscription(models_subscription.Subscription): pass

if 'builder.applications.shop' in settings.INSTALLED_APPS:
    from builder.applications.shop import models as models_shop
    class Customer(models_shop.Customer): pass

if 'builder.applications.product' in settings.INSTALLED_APPS:
    from builder.applications.product import models as models_product
    class Brand(models_product.Brand): pass
    class ProductCategory(models_product.ProductCategory): pass
    class Product(models_product.Product): pass
    class ProductFeature(models_product.ProductFeature): pass
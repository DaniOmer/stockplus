from django.contrib import admin

from stockplus.modules.subscription.models import Feature, SubscriptionPricing

class FeatureAdmin(admin.ModelAdmin):
    fields = ['name', 'description']

class SubscriptionPricingAdmin(admin.TabularInline):
    model = SubscriptionPricing
    fields = ['interval', 'price', 'currency', 'is_disable', 'stripe_id']
    readonly_fields = ['stripe_id',]
    can_delete = False
    extra = 1

class SubscriptionPlanAdmin(admin.ModelAdmin):
    inlines = [SubscriptionPricingAdmin]
    fields = ['name', 'description', 'stripe_id', 'active', 'pos_limit', 'is_free_trial', 'trial_days', 'features', 'group', 'permissions']
    readonly_fields = ['stripe_id',]

class SubscriptionAdmin(admin.ModelAdmin):
    fields = ['user', 'subscription_plan', 'interval', 'start_date', 'end_date', 'renewal_date', 'status']

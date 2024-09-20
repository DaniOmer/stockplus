from django.contrib import admin

from builder.models import Feature, SubscriptionPricing

class FeatureAdmin(admin.ModelAdmin):
    fields = ['name', 'description']

class SubscriptionPricingAdmin(admin.TabularInline):
    model = SubscriptionPricing
    fields = ['interval', 'price', 'currency', 'is_disable']
    # readonly_fields = ['is_disable',]
    extra = 1

class SubscriptionPlanAdmin(admin.ModelAdmin):
    inlines = [SubscriptionPricingAdmin]
    fields = ['name', 'description', 'active', 'features', 'group', 'permissions']

class SubscriptionAdmin(admin.ModelAdmin):
    fields = ['user', 'subscription_plan', 'interval', 'start_date', 'end_date', 'renewal_date', 'status']

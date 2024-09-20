from django.contrib import admin

from builder.models import Feature, SubscriptionPricing

class FeatureAdmin(admin.ModelAdmin):
    fields = ['name', 'description']

class SubscriptionPricingAdmin(admin.TabularInline):
    model = SubscriptionPricing
    fields = ['duration_choice', 'price', 'currency']
    extra = 1

class SubscriptionPlanAdmin(admin.ModelAdmin):
    inlines = [SubscriptionPricingAdmin]
    fields = ['name', 'description', 'active', 'features', 'group', 'permissions']

class SubscriptionAdmin(admin.ModelAdmin):
    fields = ['user', 'subscription_plan', 'duration_choice', 'start_date', 'end_date', 'renewal_date', 'status']

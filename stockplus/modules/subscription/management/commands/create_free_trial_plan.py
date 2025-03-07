"""
Management command to create a default free trial plan if one doesn't exist.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from stockplus.modules.subscription.models import SubscriptionPlan, SubscriptionPricing, Feature


class Command(BaseCommand):
    help = 'Create a default free trial plan if one doesn\'t exist'

    def handle(self, *args, **options):
        """
        Create a default free trial plan if one doesn't exist.
        """
        # Check if a free trial plan already exists
        free_trial_plan = SubscriptionPlan.objects.filter(is_free_trial=True).first()
        
        if free_trial_plan:
            self.stdout.write(self.style.SUCCESS(f"Free trial plan already exists: {free_trial_plan.name}"))
            return
        
        # Create a group for the free trial plan
        group_name = "Free Trial"
        group, created = Group.objects.get_or_create(name=group_name)
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created group: {group_name}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Group already exists: {group_name}"))
        
        # Create the free trial plan
        free_trial_plan = SubscriptionPlan.objects.create(
            name="Free Trial",
            description="30-day free trial with basic features",
            active=True,
            group=group,
            pos_limit=1,  # Limit to 1 POS during free trial
            is_free_trial=True,
            trial_days=30
        )
        
        self.stdout.write(self.style.SUCCESS(f"Created free trial plan: {free_trial_plan.name}"))
        
        # Add permissions to the group
        content_type_app_label = "stockplus"
        permission_codenames = ["stater"]  # Basic permissions for free trial
        
        for codename in permission_codenames:
            permissions = Permission.objects.filter(
                content_type__app_label=content_type_app_label,
                codename=codename
            )
            
            for permission in permissions:
                group.permissions.add(permission)
                self.stdout.write(self.style.SUCCESS(f"Added permission {permission.codename} to group {group.name}"))
        
        # Create pricing for the free trial plan (price = 0)
        pricing = SubscriptionPricing.objects.create(
            subscription_plan=free_trial_plan,
            interval="month",
            price=0,
            currency="eur"
        )
        
        self.stdout.write(self.style.SUCCESS(f"Created pricing for free trial plan: {pricing}"))
        
        # Add some features to the free trial plan
        features = [
            {"name": "Basic Inventory Management", "description": "Manage your inventory with basic features"},
            {"name": "Single Point of Sale", "description": "Create and manage a single point of sale"},
            {"name": "Basic Reporting", "description": "Access basic sales and inventory reports"}
        ]
        
        for feature_data in features:
            feature, created = Feature.objects.get_or_create(
                name=feature_data["name"],
                defaults={"description": feature_data["description"]}
            )
            
            free_trial_plan.features.add(feature)
            self.stdout.write(self.style.SUCCESS(f"Added feature to free trial plan: {feature.name}"))
        
        self.stdout.write(self.style.SUCCESS("Free trial plan created successfully"))

from django.core.management.base import BaseCommand

from builder.models import SubscriptionPlan

class Command(BaseCommand):
    help = "Synchronize groups and permissions for each subscription plan."
    
    def handle(self, *args, **options):
        susbscription = SubscriptionPlan.objects.all()

        for obj in susbscription:
           group = obj.group
           permissions = obj.permissions.all()
           group.permissions.set(permissions)

           self.stdout.write(self.style.SUCCESS(f"Successfully synced permissions and group for this subscription plan : {obj.name}."))
        self.stdout.write(self.style.SUCCESS("Sync completed successfully."))
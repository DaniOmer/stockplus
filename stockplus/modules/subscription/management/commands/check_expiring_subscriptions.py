"""
Management command to check for expiring subscriptions and send notifications.
"""

import logging
from django.core.management.base import BaseCommand
from stockplus.modules.subscription.services.subscription_service import SubscriptionService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Management command to check for expiring subscriptions and send notifications.
    """
    help = 'Check for subscriptions that are about to expire and send notifications'
    
    def handle(self, *args, **options):
        """
        Handle the command.
        """
        self.stdout.write('Checking for expiring subscriptions...')
        
        try:
            # Check for expiring subscriptions
            SubscriptionService.check_expiring_subscriptions()
            
            self.stdout.write(self.style.SUCCESS('Successfully checked for expiring subscriptions'))
        except Exception as e:
            logger.error(f"Error checking for expiring subscriptions: {e}")
            self.stdout.write(self.style.ERROR(f"Error checking for expiring subscriptions: {e}"))

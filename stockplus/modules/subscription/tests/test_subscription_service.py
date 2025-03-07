"""
Tests for the subscription service.
"""

import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from stockplus.modules.subscription.models import Subscription, SubscriptionPlan
from stockplus.modules.subscription.services.subscription_service import SubscriptionService
from stockplus.modules.company.infrastructure.models import Company
from stockplus.modules.pointofsale.infrastructure.models import PointOfSale

User = get_user_model()


class SubscriptionServiceTestCase(TestCase):
    """
    Test case for the subscription service.
    """
    
    def setUp(self):
        """
        Set up the test case.
        """
        # Create a user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password',
            first_name='Test',
            last_name='User'
        )
        
        # Create a company
        self.company = Company.objects.create(
            name='Test Company',
            owner=self.user
        )
        
        # Create subscription plans
        self.starter_plan = SubscriptionPlan.objects.create(
            name='Starter',
            description='Starter plan',
            active=True
        )
        
        self.premium_plan = SubscriptionPlan.objects.create(
            name='Premium',
            description='Premium plan',
            active=True
        )
    
    @patch('stockplus.modules.subscription.services.subscription_service.logger')
    def test_create_subscription(self, mock_logger):
        """
        Test creating a subscription.
        """
        # Create a subscription
        subscription = SubscriptionService.create_subscription(
            user=self.user,
            company=self.company,
            subscription_plan=self.starter_plan,
            interval='month'
        )
        
        # Check that the subscription was created
        self.assertIsNotNone(subscription)
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.company, self.company)
        self.assertEqual(subscription.subscription_plan, self.starter_plan)
        self.assertEqual(subscription.interval, 'month')
        self.assertEqual(subscription.status, 'pending')
        
        # Check that the logger was called
        mock_logger.info.assert_called_once_with(
            f"Created subscription for user {self.user.id} with plan {self.starter_plan.name}"
        )
    
    def test_activate_subscription(self):
        """
        Test activating a subscription.
        """
        # Create a subscription
        subscription = Subscription.objects.create(
            user=self.user,
            company=self.company,
            subscription_plan=self.starter_plan,
            interval='month',
            status='pending',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            renewal_date=timezone.now() + timedelta(days=30)
        )
        
        # Activate the subscription
        activated_subscription = SubscriptionService.activate_subscription(subscription.id)
        
        # Check that the subscription was activated
        self.assertIsNotNone(activated_subscription)
        self.assertEqual(activated_subscription.status, 'active')
    
    @patch('stockplus.modules.subscription.services.subscription_service.stripe')
    @patch('stockplus.modules.subscription.services.subscription_service.logger')
    def test_change_subscription_plan(self, mock_logger, mock_stripe):
        """
        Test changing a subscription plan.
        """
        # Create a subscription
        subscription = Subscription.objects.create(
            user=self.user,
            company=self.company,
            subscription_plan=self.starter_plan,
            interval='month',
            status='active',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            renewal_date=timezone.now() + timedelta(days=30)
        )
        
        # Create some Points of Sale
        for i in range(5):
            PointOfSale.objects.create(
                name=f'POS {i}',
                company=self.company,
                is_disable=False
            )
        
        # Change the subscription plan
        updated_subscription = SubscriptionService.change_subscription_plan(
            subscription.id,
            self.premium_plan.id
        )
        
        # Check that the subscription was updated
        self.assertIsNotNone(updated_subscription)
        self.assertEqual(updated_subscription.subscription_plan, self.premium_plan)
        
        # Check that no Points of Sale were deactivated (Premium plan allows 10)
        self.assertEqual(
            PointOfSale.objects.filter(company=self.company, is_disable=False).count(),
            5
        )
        
        # Now change back to Starter plan
        updated_subscription = SubscriptionService.change_subscription_plan(
            subscription.id,
            self.starter_plan.id
        )
        
        # Check that the subscription was updated
        self.assertIsNotNone(updated_subscription)
        self.assertEqual(updated_subscription.subscription_plan, self.starter_plan)
        
        # Check that excess Points of Sale were deactivated (Starter plan allows 3)
        self.assertEqual(
            PointOfSale.objects.filter(company=self.company, is_disable=False).count(),
            3
        )
        
        # Check that the logger was called
        mock_logger.info.assert_called_with(
            f"Deactivated 2 excess Points of Sale for company {self.company.id}"
        )
    
    @patch('stockplus.modules.subscription.services.subscription_service.send_mail_message')
    @patch('stockplus.modules.subscription.services.subscription_service.logger')
    def test_check_expiring_subscriptions(self, mock_logger, mock_send_mail):
        """
        Test checking for expiring subscriptions.
        """
        # Create a subscription that expires in 3 days
        expiry_date = timezone.now() + timedelta(days=3)
        subscription = Subscription.objects.create(
            user=self.user,
            company=self.company,
            subscription_plan=self.starter_plan,
            interval='month',
            status='active',
            start_date=timezone.now(),
            end_date=expiry_date,
            renewal_date=expiry_date
        )
        
        # Check for expiring subscriptions
        SubscriptionService.check_expiring_subscriptions()
        
        # Check that the email was sent
        mock_send_mail.assert_called_once()
        
        # Check that the logger was called
        mock_logger.info.assert_called_once_with(
            f"Sent subscription expiry notification to {self.user.email}"
        )


if __name__ == '__main__':
    unittest.main()

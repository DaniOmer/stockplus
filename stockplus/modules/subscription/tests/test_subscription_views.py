"""
Tests for the subscription views.
"""

import json
import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta
import uuid

from stockplus.modules.subscription.models import Subscription, SubscriptionPlan
from stockplus.modules.company.infrastructure.models import Company

User = get_user_model()


class SubscriptionViewsTestCase(TestCase):
    """
    Test case for the subscription views.
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
        
        # Set the company ID on the user
        self.user.company_id = self.company.id
        self.user.save()
        
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
        
        # Create a client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_list_subscription_plans(self):
        """
        Test listing subscription plans.
        """
        url = reverse('subscription_plan-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    @patch('stockplus.modules.subscription.services.subscription_service.SubscriptionService.create_subscription')
    @patch('stockplus.modules.subscription.services.subscription_service.SubscriptionService.activate_subscription')
    def test_subscribe(self, mock_activate, mock_create):
        """
        Test subscribing to a plan.
        """
        # Mock the create_subscription method
        subscription = MagicMock()
        subscription.id = uuid.uuid4()
        subscription.subscription_plan = self.starter_plan
        subscription.interval = 'month'
        subscription.start_date = timezone.now()
        subscription.end_date = timezone.now() + timedelta(days=30)
        subscription.renewal_date = timezone.now() + timedelta(days=30)
        subscription.status = 'active'
        mock_create.return_value = subscription
        
        # Mock the activate_subscription method
        mock_activate.return_value = subscription
        
        # Subscribe to a plan
        url = reverse('subscription-subscribe')
        data = {
            'plan_id': str(self.starter_plan.id),
            'interval': 'month'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Subscription created successfully')
        
        # Check that the create_subscription method was called
        mock_create.assert_called_once_with(
            user=self.user,
            company_id=self.company.id,
            subscription_plan=self.starter_plan,
            interval='month'
        )
        
        # Check that the activate_subscription method was called
        mock_activate.assert_called_once_with(subscription.id)
    
    @patch('stockplus.modules.subscription.services.subscription_service.SubscriptionService.get_user_subscription')
    @patch('stockplus.modules.subscription.services.subscription_service.SubscriptionService.cancel_subscription')
    def test_cancel(self, mock_cancel, mock_get):
        """
        Test cancelling a subscription.
        """
        # Mock the get_user_subscription method
        subscription = MagicMock()
        subscription.id = uuid.uuid4()
        mock_get.return_value = subscription
        
        # Mock the cancel_subscription method
        mock_cancel.return_value = subscription
        
        # Cancel the subscription
        url = reverse('subscription-cancel')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Subscription cancelled successfully')
        
        # Check that the get_user_subscription method was called
        mock_get.assert_called_once_with(self.user.id)
        
        # Check that the cancel_subscription method was called
        mock_cancel.assert_called_once_with(subscription.id)
    
    @patch('stockplus.modules.subscription.services.subscription_service.SubscriptionService.get_user_subscription')
    @patch('stockplus.modules.subscription.services.subscription_service.SubscriptionService.get_subscription_plan')
    @patch('stockplus.modules.subscription.services.subscription_service.SubscriptionService.change_subscription_plan')
    def test_change_plan(self, mock_change, mock_get_plan, mock_get_subscription):
        """
        Test changing a subscription plan.
        """
        # Mock the get_user_subscription method
        subscription = MagicMock()
        subscription.id = uuid.uuid4()
        mock_get_subscription.return_value = subscription
        
        # Mock the get_subscription_plan method
        mock_get_plan.return_value = self.premium_plan
        
        # Mock the change_subscription_plan method
        updated_subscription = MagicMock()
        updated_subscription.id = subscription.id
        updated_subscription.subscription_plan = self.premium_plan
        updated_subscription.interval = 'month'
        updated_subscription.start_date = timezone.now()
        updated_subscription.end_date = timezone.now() + timedelta(days=30)
        updated_subscription.renewal_date = timezone.now() + timedelta(days=30)
        updated_subscription.status = 'active'
        mock_change.return_value = updated_subscription
        
        # Change the subscription plan
        url = reverse('subscription-change-plan')
        data = {
            'plan_id': str(self.premium_plan.id)
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Subscription plan changed successfully')
        
        # Check that the get_user_subscription method was called
        mock_get_subscription.assert_called_once_with(self.user.id)
        
        # Check that the get_subscription_plan method was called
        mock_get_plan.assert_called_once_with(str(self.premium_plan.id))
        
        # Check that the change_subscription_plan method was called
        mock_change.assert_called_once_with(subscription.id, self.premium_plan.id)
    
    @patch('stockplus.modules.subscription.services.subscription_service.SubscriptionService.get_payment_history')
    def test_payment_history(self, mock_get_history):
        """
        Test getting payment history.
        """
        # Mock the get_payment_history method
        payment_history = [
            {
                'id': 'inv_123',
                'amount': 10.00,
                'currency': 'USD',
                'status': 'paid',
                'date': timezone.now(),
                'invoice_url': 'https://example.com/invoice/123'
            }
        ]
        mock_get_history.return_value = payment_history
        
        # Get the payment history
        url = reverse('subscription-payment-history')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payment_history'], payment_history)
        
        # Check that the get_payment_history method was called
        mock_get_history.assert_called_once_with(self.user.id)


if __name__ == '__main__':
    unittest.main()

"""
Subscription services for the subscription application.
This module contains the services for the subscription application.
"""

import logging
import stripe
import sentry_sdk
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.db import transaction

from stockplus.modules.subscription.models import Subscription, SubscriptionPlan
from stockplus.modules.pointofsale.infrastructure.models import PointOfSale
from stockplus.modules.messenger.infrastructure.utils import send_mail_message

logger = logging.getLogger(__name__)

# Configure Stripe API key
if hasattr(settings, 'STRIPE_SECRET_KEY'):
    stripe.api_key = settings.STRIPE_SECRET_KEY
else:
    logger.error("STRIPE_SECRET_KEY is not set in settings. Stripe integration will not work.")


class SubscriptionService:
    """
    Service for managing subscriptions.
    """
    
    @staticmethod
    def get_subscription_plans():
        """
        Get all active subscription plans.
        
        Returns:
            QuerySet: All active subscription plans
        """
        return SubscriptionPlan.objects.filter(active=True)
    
    @staticmethod
    def get_subscription_plan(plan_id):
        """
        Get a subscription plan by ID.
        
        Args:
            plan_id: The ID of the subscription plan
            
        Returns:
            SubscriptionPlan: The subscription plan
        """
        try:
            return SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_subscription(user_id):
        """
        Get a user's subscription.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            Subscription: The user's subscription
        """
        try:
            return Subscription.objects.get(user_id=user_id)
        except Subscription.DoesNotExist:
            return None
    
    @staticmethod
    @transaction.atomic
    def create_subscription(user, company, subscription_plan, interval='month'):
        """
        Create a subscription for a user.
        
        Args:
            user: The user
            company: The company
            subscription_plan: The subscription plan
            interval: The subscription interval
            
        Returns:
            Subscription: The created subscription
        """
        try:
            # Create the subscription
            subscription = Subscription(
                user=user,
                company=company,
                subscription_plan=subscription_plan,
                interval=interval,
                status='pending'
            )
            
            # Set the dates
            subscription.pre_activate()
            
            # Save the subscription
            subscription.save()
            
            logger.info(f"Created subscription for user {user.id} with plan {subscription_plan.name}")
            
            return subscription
        except Exception as e:
            logger.error(f"Error creating subscription: {e}")
            sentry_sdk.capture_exception(e)
            raise
    
    @staticmethod
    def activate_subscription(subscription_id):
        """
        Activate a subscription.
        
        Args:
            subscription_id: The ID of the subscription
            
        Returns:
            Subscription: The activated subscription
        """
        try:
            subscription = Subscription.objects.get(id=subscription_id)
            subscription.activate()
            return subscription
        except Subscription.DoesNotExist:
            return None
    
    @staticmethod
    def cancel_subscription(subscription_id):
        """
        Cancel a subscription.
        
        Args:
            subscription_id: The ID of the subscription
            
        Returns:
            Subscription: The cancelled subscription
        """
        try:
            subscription = Subscription.objects.get(id=subscription_id)
            
            # Cancel the subscription in Stripe if it has a Stripe ID
            if hasattr(subscription, 'stripe_id') and subscription.stripe_id:
                try:
                    stripe.Subscription.delete(subscription.stripe_id)
                except Exception as e:
                    logger.error(f"Error cancelling Stripe subscription: {e}")
            
            # Cancel the subscription locally
            subscription.cancel()
            
            return subscription
        except Subscription.DoesNotExist:
            return None
    
    @staticmethod
    @transaction.atomic
    def change_subscription_plan(subscription_id, new_plan_id):
        """
        Change a subscription's plan.
        
        Args:
            subscription_id: The ID of the subscription
            new_plan_id: The ID of the new subscription plan
            
        Returns:
            Subscription: The updated subscription
        """
        try:
            subscription = Subscription.objects.get(id=subscription_id)
            new_plan = SubscriptionPlan.objects.get(id=new_plan_id)
            
            # Check if the new plan has a lower Point of Sale limit
            if new_plan.name == 'Starter':
                pos_limit = 3
            elif new_plan.name == 'Premium':
                pos_limit = 10
            else:
                pos_limit = 0
            
            # Count the company's active Points of Sale
            pos_count = PointOfSale.objects.filter(
                company_id=subscription.company_id,
                is_disable=False
            ).count()
            
            # If the company has more Points of Sale than the new plan allows,
            # deactivate the excess Points of Sale
            if pos_count > pos_limit and pos_limit > 0:
                # Get the excess Points of Sale
                excess_pos = PointOfSale.objects.filter(
                    company_id=subscription.company_id,
                    is_disable=False
                ).order_by('-created_at')[pos_limit:]
                
                # Deactivate the excess Points of Sale
                for pos in excess_pos:
                    pos.is_disable = True
                    pos.save()
                
                logger.info(f"Deactivated {len(excess_pos)} excess Points of Sale for company {subscription.company_id}")
            
            # Update the subscription plan
            old_plan = subscription.subscription_plan.name
            subscription.subscription_plan = new_plan
            subscription.save()
            
            logger.info(f"Changed subscription plan for user {subscription.user.id} from {old_plan} to {new_plan.name}")
            
            # Update the subscription in Stripe if it has a Stripe ID
            if hasattr(subscription, 'stripe_id') and subscription.stripe_id:
                try:
                    stripe.Subscription.modify(
                        subscription.stripe_id,
                        items=[{
                            'id': subscription.stripe_id,
                            'price': new_plan.stripe_id
                        }]
                    )
                except Exception as e:
                    logger.error(f"Error updating Stripe subscription: {e}")
                    sentry_sdk.capture_exception(e)
            
            return subscription
        except Subscription.DoesNotExist:
            logger.error(f"Subscription with ID {subscription_id} not found")
            return None
        except SubscriptionPlan.DoesNotExist:
            logger.error(f"Subscription plan with ID {new_plan_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error changing subscription plan: {e}")
            sentry_sdk.capture_exception(e)
            raise
    
    @staticmethod
    def check_expiring_subscriptions():
        """
        Check for subscriptions that are about to expire and send notifications.
        """
        # Get subscriptions that expire in 3 days
        expiry_date = timezone.now() + timedelta(days=3)
        expiring_subscriptions = Subscription.objects.filter(
            end_date__date=expiry_date.date(),
            status='active'
        )
        
        # Send notifications for each expiring subscription
        for subscription in expiring_subscriptions:
            try:
                # Send email notification
                if subscription.user.email:
                    send_mail_message(
                        subject='Your subscription is about to expire',
                        target=subscription.user.email,
                        message=f'Your {subscription.subscription_plan.name} subscription will expire in 3 days. Please renew your subscription to continue using the service.',
                        html=f'<p>Your {subscription.subscription_plan.name} subscription will expire in 3 days. Please renew your subscription to continue using the service.</p>'
                    )
                    logger.info(f"Sent subscription expiry notification to {subscription.user.email}")
            except Exception as e:
                logger.error(f"Error sending subscription expiry notification: {e}")
    
    @staticmethod
    def get_payment_history(user_id):
        """
        Get a user's payment history.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            list: The user's payment history
        """
        try:
            # Get the user's subscription
            subscription = Subscription.objects.get(user_id=user_id)
            
            # If the subscription has a Stripe ID, get the payment history from Stripe
            if hasattr(subscription, 'stripe_id') and subscription.stripe_id:
                try:
                    # Get the Stripe customer ID
                    customer = stripe.Customer.retrieve(subscription.user.stripe_customer_id)
                    
                    # Get the customer's invoices
                    invoices = stripe.Invoice.list(customer=customer.id)
                    
                    # Format the invoices
                    payment_history = []
                    for invoice in invoices.data:
                        payment_history.append({
                            'id': invoice.id,
                            'amount': invoice.amount_paid / 100,  # Convert from cents
                            'currency': invoice.currency,
                            'status': invoice.status,
                            'date': datetime.fromtimestamp(invoice.created),
                            'invoice_url': invoice.hosted_invoice_url
                        })
                    
                    return payment_history
                except Exception as e:
                    logger.error(f"Error getting Stripe payment history: {e}")
                    return []
            
            # If the subscription doesn't have a Stripe ID, return an empty list
            return []
        except Subscription.DoesNotExist:
            return []

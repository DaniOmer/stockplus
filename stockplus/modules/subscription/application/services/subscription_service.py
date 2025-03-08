"""
Subscription services for the subscription application.
This module contains the services for the subscription application.
"""

import logging
import stripe
import sentry_sdk
from datetime import datetime, timedelta
from typing import List, Optional
from django.conf import settings
from django.utils import timezone
from django.db import transaction

from stockplus.modules.subscription.application.interfaces import (
    ISubscriptionPlanRepository,
    ISubscriptionRepository
)
from stockplus.modules.subscription.domain.entities import (
    SubscriptionPlan,
    Subscription
)
from stockplus.modules.subscription.domain.exceptions import (
    SubscriptionNotFoundError,
    SubscriptionPlanNotFoundError,
    SubscriptionAlreadyExistsError,
    SubscriptionStatusError
)
from stockplus.modules.subscription.infrastructure.utils import (
    add_users_to_subscription_group,
    remove_users_from_subscription_group
)
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
    def __init__(self, 
                subscription_repository: ISubscriptionRepository,
                subscription_plan_repository: ISubscriptionPlanRepository):
        self.subscription_repository = subscription_repository
        self.subscription_plan_repository = subscription_plan_repository
    
    def get_subscription_plans(self) -> List[SubscriptionPlan]:
        """
        Get all active subscription plans.
        
        Returns:
            QuerySet: All active subscription plans
        """
        return self.subscription_plan_repository.get_all_active()
    
    def get_subscription_plan(self, plan_id: int) -> Optional[SubscriptionPlan]:
        """
        Get a subscription plan by ID.
        
        Args:
            plan_id: The ID of the subscription plan
            
        Returns:
            SubscriptionPlan: The subscription plan
        """
        plan = self.subscription_plan_repository.get_by_id(plan_id)
        if not plan:
            raise SubscriptionPlanNotFoundError(plan_id)
        return plan
    
    def get_user_subscription(self, user_id: int) -> Optional[Subscription]:
        """
        Get a user's subscription.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            Subscription: The user's subscription
        """
        return self.subscription_repository.get_by_user_id(user_id)
    
    @transaction.atomic
    def create_subscription(self, user, company, subscription_plan, interval='month'):
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
            # Check if the user already has a subscription
            existing_subscription = self.get_user_subscription(user.id)
            if existing_subscription:
                raise SubscriptionAlreadyExistsError(user.id)
            
            # Create the subscription
            subscription = Subscription(
                user_id=user.id,
                company_id=company.id if company else None,
                subscription_plan_id=subscription_plan.id,
                interval=interval,
                status='pending'
            )
            
            # Set the dates
            self._pre_activate(subscription)
            
            # Save the subscription
            created_subscription = self.subscription_repository.create(subscription)
            
            logger.info(f"Created subscription for user {user.id} with plan {subscription_plan.name}")
            
            return created_subscription
        except Exception as e:
            logger.error(f"Error creating subscription: {e}")
            sentry_sdk.capture_exception(e)
            raise
    
    def activate_subscription(self, subscription_id: int) -> Subscription:
        """
        Activate a subscription.
        
        Args:
            subscription_id: The ID of the subscription
            
        Returns:
            Subscription: The activated subscription
        """
        subscription = self.subscription_repository.get_by_id(subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError(subscription_id)
        
        if subscription.status != 'pending':
            raise SubscriptionStatusError(
                subscription_id, 
                subscription.status, 
                'active'
            )
        
        subscription.status = 'active'
        updated_subscription = self.subscription_repository.update(subscription)
        
        # Add users to subscription group
        add_users_to_subscription_group(updated_subscription)
        
        return updated_subscription
    
    def cancel_subscription(self, subscription_id: int) -> Subscription:
        """
        Cancel a subscription.
        
        Args:
            subscription_id: The ID of the subscription
            
        Returns:
            Subscription: The cancelled subscription
        """
        subscription = self.subscription_repository.get_by_id(subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError(subscription_id)
        
        # Cancel the subscription in Stripe if it has a Stripe ID
        if hasattr(subscription, 'stripe_id') and subscription.stripe_id:
            try:
                stripe.Subscription.delete(subscription.stripe_id)
            except Exception as e:
                logger.error(f"Error cancelling Stripe subscription: {e}")
        
        # Cancel the subscription locally
        subscription.status = 'cancelled'
        updated_subscription = self.subscription_repository.update(subscription)
        
        return updated_subscription
    
    @transaction.atomic
    def change_subscription_plan(self, subscription_id: int, new_plan_id: int) -> Subscription:
        """
        Change a subscription's plan.
        
        Args:
            subscription_id: The ID of the subscription
            new_plan_id: The ID of the new subscription plan
            
        Returns:
            Subscription: The updated subscription
        """
        try:
            subscription = self.subscription_repository.get_by_id(subscription_id)
            if not subscription:
                raise SubscriptionNotFoundError(subscription_id)
            
            new_plan = self.subscription_plan_repository.get_by_id(new_plan_id)
            if not new_plan:
                raise SubscriptionPlanNotFoundError(new_plan_id)
            
            # Check if the new plan has a lower Point of Sale limit
            pos_limit = new_plan.pos_limit
            
            # Count the company's active Points of Sale
            if subscription.company_id:
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
            old_plan_id = subscription.subscription_plan_id
            subscription.subscription_plan_id = new_plan.id
            updated_subscription = self.subscription_repository.update(subscription)
            
            logger.info(f"Changed subscription plan for user {subscription.user_id} from {old_plan_id} to {new_plan.id}")
            
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
            
            return updated_subscription
        except (SubscriptionNotFoundError, SubscriptionPlanNotFoundError):
            raise
        except Exception as e:
            logger.error(f"Error changing subscription plan: {e}")
            sentry_sdk.capture_exception(e)
            raise
    
    def check_expiring_subscriptions(self):
        """
        Check for subscriptions that are about to expire and send notifications.
        """
        # Get subscriptions that expire in 3 days
        expiry_date = timezone.now() + timedelta(days=3)
        expiring_subscriptions = self.subscription_repository.get_expiring_subscriptions(expiry_date)
        
        # Send notifications for each expiring subscription
        for subscription in expiring_subscriptions:
            try:
                # Get the user's email
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(id=subscription.user_id)
                
                # Get the subscription plan name
                plan = self.subscription_plan_repository.get_by_id(subscription.subscription_plan_id)
                plan_name = plan.name if plan else "Unknown"
                
                # Send email notification
                if user.email:
                    send_mail_message(
                        subject='Your subscription is about to expire',
                        target=user.email,
                        message=f'Your {plan_name} subscription will expire in 3 days. Please renew your subscription to continue using the service.',
                        html=f'<p>Your {plan_name} subscription will expire in 3 days. Please renew your subscription to continue using the service.</p>'
                    )
                    logger.info(f"Sent subscription expiry notification to {user.email}")
            except Exception as e:
                logger.error(f"Error sending subscription expiry notification: {e}")
    
    def expire_subscription(self, subscription_id: int) -> Subscription:
        """
        Expire a subscription.
        
        Args:
            subscription_id: The ID of the subscription
            
        Returns:
            Subscription: The expired subscription
        """
        subscription = self.subscription_repository.get_by_id(subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError(subscription_id)
        
        subscription.status = 'expired'
        updated_subscription = self.subscription_repository.update(subscription)
        
        # Remove users from subscription group
        remove_users_from_subscription_group(updated_subscription)
        
        return updated_subscription
    
    def get_payment_history(self, user_id: int) -> List[dict]:
        """
        Get a user's payment history.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            list: The user's payment history
        """
        try:
            # Get the user's subscription
            subscription = self.get_user_subscription(user_id)
            
            if not subscription:
                return []
            
            # If the subscription has a Stripe ID, get the payment history from Stripe
            if hasattr(subscription, 'stripe_id') and subscription.stripe_id:
                try:
                    # Get the Stripe customer ID
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    user = User.objects.get(id=user_id)
                    
                    if not hasattr(user, 'stripe_customer_id'):
                        return []
                    
                    # Get the customer's invoices
                    customer = stripe.Customer.retrieve(user.stripe_customer_id)
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
        except Exception as e:
            logger.error(f"Error getting payment history: {e}")
            return []
    
    def _pre_activate(self, subscription: Subscription) -> None:
        """
        Set the dates for a subscription before activation.
        
        Args:
            subscription: The subscription to pre-activate
        """
        subscription.start_date = timezone.now()
        
        if subscription.interval == 'month':
            subscription.end_date = subscription.start_date + timedelta(days=30)
        elif subscription.interval == 'semester':
            subscription.end_date = subscription.start_date + timedelta(days=180)
        elif subscription.interval == 'year':
            subscription.end_date = subscription.start_date + timedelta(days=365)
        
        subscription.renewal_date = subscription.end_date

"""
Subscription views for the subscription application.
This module contains the views for the subscription application.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Custom throttle classes
class SubscriptionRateThrottle(UserRateThrottle):
    rate = '10/minute'  # Limit to 10 requests per minute for authenticated users

class SubscriptionAnonRateThrottle(AnonRateThrottle):
    rate = '3/minute'  # Limit to 3 requests per minute for anonymous users

from stockplus.modules.subscription.models import SubscriptionPlan, Subscription
from stockplus.modules.subscription.serializers import (
    SubscriptionPlanSerializer,
    SubscriptionPricingSerializer,
    FeatureSerializer,
    SubscriptionSerializer,
    SubscribeSerializer,
    ChangePlanSerializer
)
from stockplus.modules.subscription.services.subscription_service import SubscriptionService


class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view subscription plans.
    """
    queryset = SubscriptionPlan.objects.filter(active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [SubscriptionRateThrottle]


class SubscriptionViewSet(viewsets.ViewSet):
    """
    API endpoint to manage subscriptions.
    """
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [SubscriptionRateThrottle]
    
    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action == 'subscribe':
            return SubscribeSerializer
        elif self.action == 'change_plan':
            return ChangePlanSerializer
        return SubscriptionSerializer
    
    def list(self, request):
        """
        Get the user's subscription.
        """
        subscription = SubscriptionService.get_user_subscription(request.user.id)
        
        if not subscription:
            return Response({
                'message': 'No subscription found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'id': subscription.id,
            'plan': {
                'id': subscription.subscription_plan.id,
                'name': subscription.subscription_plan.name,
                'description': subscription.subscription_plan.description
            },
            'interval': subscription.interval,
            'start_date': subscription.start_date,
            'end_date': subscription.end_date,
            'renewal_date': subscription.renewal_date,
            'status': subscription.status
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        """
        Subscribe to a plan.
        """
        plan_id = request.data.get('plan_id')
        interval = request.data.get('interval', 'month')
        
        if not plan_id:
            return Response({
                'message': 'Plan ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the subscription plan
        plan = SubscriptionService.get_subscription_plan(plan_id)
        
        if not plan:
            return Response({
                'message': 'Subscription plan not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the user already has a subscription
        existing_subscription = SubscriptionService.get_user_subscription(request.user.id)
        
        if existing_subscription:
            return Response({
                'message': 'User already has a subscription'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the subscription
        subscription = SubscriptionService.create_subscription(
            user=request.user,
            company_id=request.user.company_id,
            subscription_plan=plan,
            interval=interval
        )
        
        # Activate the subscription
        SubscriptionService.activate_subscription(subscription.id)
        
        return Response({
            'message': 'Subscription created successfully',
            'subscription': {
                'id': subscription.id,
                'plan': {
                    'id': subscription.subscription_plan.id,
                    'name': subscription.subscription_plan.name,
                    'description': subscription.subscription_plan.description
                },
                'interval': subscription.interval,
                'start_date': subscription.start_date,
                'end_date': subscription.end_date,
                'renewal_date': subscription.renewal_date,
                'status': subscription.status
            }
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def cancel(self, request):
        """
        Cancel the user's subscription.
        """
        subscription = SubscriptionService.get_user_subscription(request.user.id)
        
        if not subscription:
            return Response({
                'message': 'No subscription found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Cancel the subscription
        SubscriptionService.cancel_subscription(subscription.id)
        
        return Response({
            'message': 'Subscription cancelled successfully'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def change_plan(self, request):
        """
        Change the user's subscription plan.
        """
        plan_id = request.data.get('plan_id')
        
        if not plan_id:
            return Response({
                'message': 'Plan ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the subscription plan
        plan = SubscriptionService.get_subscription_plan(plan_id)
        
        if not plan:
            return Response({
                'message': 'Subscription plan not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get the user's subscription
        subscription = SubscriptionService.get_user_subscription(request.user.id)
        
        if not subscription:
            return Response({
                'message': 'No subscription found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Change the subscription plan
        updated_subscription = SubscriptionService.change_subscription_plan(subscription.id, plan.id)
        
        return Response({
            'message': 'Subscription plan changed successfully',
            'subscription': {
                'id': updated_subscription.id,
                'plan': {
                    'id': updated_subscription.subscription_plan.id,
                    'name': updated_subscription.subscription_plan.name,
                    'description': updated_subscription.subscription_plan.description
                },
                'interval': updated_subscription.interval,
                'start_date': updated_subscription.start_date,
                'end_date': updated_subscription.end_date,
                'renewal_date': updated_subscription.renewal_date,
                'status': updated_subscription.status
            }
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def payment_history(self, request):
        """
        Get the user's payment history.
        """
        payment_history = SubscriptionService.get_payment_history(request.user.id)
        
        return Response({
            'payment_history': payment_history
        }, status=status.HTTP_200_OK)

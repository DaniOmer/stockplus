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

from stockplus.modules.subscription.infrastructure.models import SubscriptionPlan
from stockplus.modules.subscription.interfaces.serializers import (
    SubscriptionPlanSerializer,
    SubscriptionSerializer,
    SubscribeSerializer,
    ChangePlanSerializer
)
from stockplus.modules.subscription.application.services import SubscriptionService
from stockplus.modules.subscription.domain.exceptions import (
    SubscriptionNotFoundError,
    SubscriptionPlanNotFoundError,
    SubscriptionAlreadyExistsError,
    SubscriptionStatusError
)


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
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subscription_service = None
    
    def get_subscription_service(self) -> SubscriptionService:
        """
        Get the subscription service from the dependency container.
        
        Returns:
            The subscription service.
        """
        if not self.subscription_service:
            from stockplus.config.dependencies import get_subscription_service
            self.subscription_service = get_subscription_service()
        return self.subscription_service
    
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
        service = self.get_subscription_service()
        subscription = service.get_user_subscription(request.user.id)
        
        if not subscription:
            return Response({
                'message': 'No subscription found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get the subscription plan
        plan = service.get_subscription_plan(subscription.subscription_plan_id)
        
        return Response({
            'id': subscription.id,
            'plan': {
                'id': plan.id,
                'name': plan.name,
                'description': plan.description
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
        
        service = self.get_subscription_service()
        
        try:
            # Get the subscription plan
            plan = service.get_subscription_plan(plan_id)
            
            # Create the subscription
            subscription = service.create_subscription(
                user=request.user,
                company=request.user.company if hasattr(request.user, 'company') else None,
                subscription_plan=plan,
                interval=interval
            )
            
            # Activate the subscription
            service.activate_subscription(subscription.id)
            
            return Response({
                'message': 'Subscription created successfully',
                'subscription': {
                    'id': subscription.id,
                    'plan': {
                        'id': plan.id,
                        'name': plan.name,
                        'description': plan.description
                    },
                    'interval': subscription.interval,
                    'start_date': subscription.start_date,
                    'end_date': subscription.end_date,
                    'renewal_date': subscription.renewal_date,
                    'status': subscription.status
                }
            }, status=status.HTTP_201_CREATED)
        except SubscriptionPlanNotFoundError:
            return Response({
                'message': 'Subscription plan not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except SubscriptionAlreadyExistsError:
            return Response({
                'message': 'User already has a subscription'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def cancel(self, request):
        """
        Cancel the user's subscription.
        """
        service = self.get_subscription_service()
        
        try:
            # Get the user's subscription
            subscription = service.get_user_subscription(request.user.id)
            
            if not subscription:
                return Response({
                    'message': 'No subscription found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Cancel the subscription
            service.cancel_subscription(subscription.id)
            
            return Response({
                'message': 'Subscription cancelled successfully'
            }, status=status.HTTP_200_OK)
        except SubscriptionNotFoundError:
            return Response({
                'message': 'No subscription found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
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
        
        service = self.get_subscription_service()
        
        try:
            # Get the user's subscription
            subscription = service.get_user_subscription(request.user.id)
            
            if not subscription:
                return Response({
                    'message': 'No subscription found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Change the subscription plan
            updated_subscription = service.change_subscription_plan(subscription.id, plan_id)
            
            # Get the subscription plan
            plan = service.get_subscription_plan(updated_subscription.subscription_plan_id)
            
            return Response({
                'message': 'Subscription plan changed successfully',
                'subscription': {
                    'id': updated_subscription.id,
                    'plan': {
                        'id': plan.id,
                        'name': plan.name,
                        'description': plan.description
                    },
                    'interval': updated_subscription.interval,
                    'start_date': updated_subscription.start_date,
                    'end_date': updated_subscription.end_date,
                    'renewal_date': updated_subscription.renewal_date,
                    'status': updated_subscription.status
                }
            }, status=status.HTTP_200_OK)
        except SubscriptionNotFoundError:
            return Response({
                'message': 'No subscription found'
            }, status=status.HTTP_404_NOT_FOUND)
        except SubscriptionPlanNotFoundError:
            return Response({
                'message': 'Subscription plan not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def payment_history(self, request):
        """
        Get the user's payment history.
        """
        service = self.get_subscription_service()
        payment_history = service.get_payment_history(request.user.id)
        
        return Response({
            'payment_history': payment_history
        }, status=status.HTTP_200_OK)

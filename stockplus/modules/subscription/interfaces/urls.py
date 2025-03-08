from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stockplus.modules.subscription.interfaces.views import (
    SubscriptionPlanViewSet,
    SubscriptionViewSet
)

router = DefaultRouter()
router.register(r'api/subscription/plan', SubscriptionPlanViewSet, basename='subscription_plan')
router.register(r'api/subscription', SubscriptionViewSet, basename='subscription')

urlpatterns = router.urls

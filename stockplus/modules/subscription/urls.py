from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stockplus.modules.subscription import views

router = DefaultRouter()
router.register(r'api/subscription/plan', views.SubscriptionPlanViewSet, basename='subscription_plan')
router.register(r'api/subscription', views.SubscriptionViewSet, basename='subscription')

urlpatterns = router.urls

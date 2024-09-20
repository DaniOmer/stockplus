from rest_framework.routers import DefaultRouter

from builder.applications.subscription import views

router = DefaultRouter()
router.register(r'api/subscription/plan', views.SubscriptionPlanViewSet, basename='subscription_plan_list')
urlpatterns = router.urls
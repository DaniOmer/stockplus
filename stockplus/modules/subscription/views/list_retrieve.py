from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.db.models import QuerySet

# Commenting out import since SubscriptionPlan is abstract
# from stockplus.models import SubscriptionPlan
from stockplus.modules.subscription.serializers import SubscriptionPlanSerializer

class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]
    # Using empty queryset since SubscriptionPlan is abstract
    queryset = QuerySet().none()

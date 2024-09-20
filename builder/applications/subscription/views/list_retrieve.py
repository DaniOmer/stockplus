from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from builder.models import SubscriptionPlan
from builder.applications.subscription.serializers import SubscriptionPlanSerializer

class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]
    queryset = SubscriptionPlan.objects.all()
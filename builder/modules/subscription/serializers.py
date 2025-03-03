from typing import List
from rest_framework import serializers

# Removed imports since models are abstract
# from builder.models import SubscriptionPlan, SubscriptionPricing, Feature

class FeatureSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

class SubscriptionPricingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    interval = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()

class SubscriptionPlanSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True, required=False)
    features = FeatureSerializer(many=True, read_only=True)
    pricing = serializers.SerializerMethodField()

    def get_pricing(self, obj) -> List[dict]:
        # Since we're using abstract models, we'll return an empty list
        # This is just a placeholder to make the schema generation work
        return []

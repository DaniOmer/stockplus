from typing import List
from rest_framework import serializers

from builder.models import SubscriptionPlan, SubscriptionPricing, Feature

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'name']

class SubscriptionPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPricing
        fields = ['id', 'interval', 'price', 'currency']

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    pricing = serializers.SerializerMethodField()

    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'description', 'features', 'pricing']

    def get_pricing(self, obj) -> List[dict]:
        interval = self.context['request'].query_params.get('interval')
        if interval is not None:
            pricing = SubscriptionPricing.objects.filter(subscription_plan=obj, interval=interval, is_disable=False)
            return SubscriptionPricingSerializer(pricing, many=True).data
        pricing = SubscriptionPricing.objects.filter(subscription_plan=obj, is_disable=False)
        return SubscriptionPricingSerializer(pricing, many=True).data
    
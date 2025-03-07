from rest_framework import serializers

from stockplus.modules.subscription.models import SubscriptionPlan, SubscriptionPricing, Feature, Subscription


class FeatureSerializer(serializers.ModelSerializer):
    """
    Serializer for the Feature model.
    """
    class Meta:
        model = Feature
        fields = ['id', 'name', 'description']


class SubscriptionPricingSerializer(serializers.ModelSerializer):
    """
    Serializer for the SubscriptionPricing model.
    """
    class Meta:
        model = SubscriptionPricing
        fields = ['id', 'interval', 'price', 'currency']


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the SubscriptionPlan model.
    """
    features = FeatureSerializer(many=True, read_only=True)
    pricing = SubscriptionPricingSerializer(many=True, read_only=True, source='pricing.all')
    
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'description', 'features', 'pricing', 'pos_limit', 'is_free_trial', 'trial_days']


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subscription model.
    """
    plan = SubscriptionPlanSerializer(source='subscription_plan', read_only=True)
    
    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'interval', 'start_date', 'end_date', 'renewal_date', 'status']


class PaymentHistorySerializer(serializers.Serializer):
    """
    Serializer for payment history.
    """
    id = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()
    status = serializers.CharField()
    date = serializers.DateTimeField()
    invoice_url = serializers.URLField(required=False)


# Action serializers for Swagger documentation

class SubscribeSerializer(serializers.Serializer):
    """
    Serializer for the subscribe action.
    """
    plan_id = serializers.UUIDField(help_text="The ID of the subscription plan")
    interval = serializers.ChoiceField(
        choices=['month', 'semester', 'year'],
        default='month',
        help_text="The subscription interval"
    )


class ChangePlanSerializer(serializers.Serializer):
    """
    Serializer for the change_plan action.
    """
    plan_id = serializers.UUIDField(help_text="The ID of the new subscription plan")

from rest_framework import serializers

from stockplus.modules.shop.infrastructure.models import (
    Customer,
    Product,
    Price
)


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """
    class Meta:
        model = Customer
        fields = ['id', 'user', 'stripe_id']


class PriceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Price model.
    """
    class Meta:
        model = Price
        fields = ['id', 'product', 'unit_amount', 'currency', 'interval', 'interval_count']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """
    prices = PriceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'active', 'prices']


# Action serializers for Swagger documentation

class CreateProductSerializer(serializers.Serializer):
    """
    Serializer for the create_product action.
    """
    name = serializers.CharField(help_text="The name of the product")
    description = serializers.CharField(required=False, help_text="The description of the product")
    active = serializers.BooleanField(default=True, help_text="Whether the product is active")


class CreatePriceSerializer(serializers.Serializer):
    """
    Serializer for the create_price action.
    """
    product_id = serializers.IntegerField(help_text="The ID of the product")
    unit_amount = serializers.IntegerField(help_text="The amount in cents")
    currency = serializers.CharField(default='eur', help_text="The currency")
    interval = serializers.ChoiceField(
        choices=['day', 'week', 'month', 'year'],
        required=False,
        help_text="The interval (day, week, month, year)"
    )
    interval_count = serializers.IntegerField(required=False, help_text="The interval count")

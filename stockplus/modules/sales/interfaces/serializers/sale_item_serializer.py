from rest_framework import serializers

from stockplus.modules.product.interfaces.serializers import ProductSerializer
from stockplus.modules.product.infrastructure.models import Product, ProductVariant
from stockplus.modules.sales.domain.entities import SaleItem
from stockplus.modules.sales.infrastructure.models import SaleItem as SaleItemORM


class SaleItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the sale item model.
    """
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    product_variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(),
        source='product_variant',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = SaleItemORM
        fields = [
            'id', 'uid', 'product', 'product_id', 'product_variant', 'product_variant_id',
            'quantity', 'unit_price', 'discount', 'total_price'
        ]
        read_only_fields = ['id', 'uid', 'total_price']
    
    def to_domain(self) -> SaleItem:
        """
        Convert the serializer data to a domain model.
        
        Returns:
            A domain model instance.
        """
        validated_data = self.validated_data
        
        return SaleItem(
            product_id=validated_data.get('product').id if 'product' in validated_data else None,
            product_variant_id=validated_data.get('product_variant').id if 'product_variant' in validated_data else None,
            quantity=validated_data.get('quantity', 1),
            unit_price=validated_data.get('unit_price', 0),
            discount=validated_data.get('discount', 0)
        )

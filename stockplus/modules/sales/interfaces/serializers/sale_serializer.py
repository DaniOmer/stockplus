from rest_framework import serializers

from stockplus.modules.product.interfaces.serializers import ProductSerializer
from stockplus.modules.product.infrastructure.models import Product
from stockplus.modules.pointofsale.interfaces.serializers import PointOfSaleSerializer
from stockplus.modules.pointofsale.infrastructure.models import PointOfSale
from stockplus.modules.sales.domain.entities import Sale, SaleItem
from stockplus.modules.sales.infrastructure.models import Sale as SaleORM
from stockplus.modules.sales.infrastructure.models import SaleItem as SaleItemORM
from stockplus.modules.sales.interfaces.serializers.sale_item_serializer import SaleItemSerializer


class SaleSerializer(serializers.ModelSerializer):
    """
    Serializer for the sale model.
    """
    items = SaleItemSerializer(many=True, source='sale_items', read_only=True)
    point_of_sale = PointOfSaleSerializer(read_only=True)
    point_of_sale_id = serializers.PrimaryKeyRelatedField(
        queryset=PointOfSale.objects.all(),
        source='point_of_sale',
        write_only=True,
        required=False,
        allow_null=True
    )
    item_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = SaleORM
        fields = [
            'id', 'uid', 'invoice_number', 'date', 'total_amount', 'payment_method',
            'items', 'point_of_sale', 'point_of_sale_id', 'item_count',
            'is_cancelled', 'cancelled_at', 'notes'
        ]
        read_only_fields = [
            'id', 'uid', 'invoice_number', 'date', 'total_amount',
            'is_cancelled', 'cancelled_at'
        ]
    
    def to_domain(self) -> Sale:
        """
        Convert the serializer data to a domain model.
        
        Returns:
            A domain model instance.
        """
        validated_data = self.validated_data
        
        # Convert items
        items = []
        if 'items' in validated_data:
            for item_data in validated_data['items']:
                item_serializer = SaleItemSerializer(data=item_data)
                item_serializer.is_valid(raise_exception=True)
                items.append(item_serializer.to_domain())
        
        return Sale(
            payment_method=validated_data.get('payment_method', 'cash'),
            point_of_sale_id=validated_data.get('point_of_sale').id if 'point_of_sale' in validated_data else None,
            notes=validated_data.get('notes'),
            items=items
        )
    
    def create(self, validated_data):
        """
        Create a new sale.
        
        Args:
            validated_data: The validated data.
            
        Returns:
            The created sale.
        """
        request = self.context.get('request')
        company = request.user.company
        
        # Extract nested data
        items_data = validated_data.pop('items', [])
        
        # Create sale
        validated_data['company'] = company
        validated_data['user'] = request.user
        sale = super().create(validated_data)
        
        # Create items
        for item_data in items_data:
            product_id = item_data.pop('product')
            product_variant_id = item_data.pop('product_variant', None)
            
            # Get product
            product = Product.objects.get(id=product_id.id)
            
            # Create item
            SaleItemORM.objects.create(
                sale=sale,
                product=product,
                product_variant_id=product_variant_id.id if product_variant_id else None,
                **item_data
            )
        
        return sale

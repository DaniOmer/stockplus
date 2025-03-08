from rest_framework import serializers

from stockplus.modules.sales.domain.entities import Invoice
from stockplus.modules.sales.infrastructure.models import Invoice as InvoiceORM
from stockplus.modules.sales.interfaces.serializers.sale_serializer import SaleSerializer


class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the invoice model.
    """
    sale = SaleSerializer(read_only=True)
    net_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    grand_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = InvoiceORM
        fields = [
            'id', 'uid', 'invoice_number', 'sale', 'date', 'due_date',
            'total_amount', 'tax_amount', 'discount_amount', 'net_amount', 'grand_total',
            'customer_name', 'customer_email', 'customer_phone', 'customer_address',
            'notes', 'is_paid', 'payment_date'
        ]
        read_only_fields = [
            'id', 'uid', 'invoice_number', 'sale', 'date', 'total_amount',
            'net_amount', 'grand_total', 'payment_date'
        ]
    
    def to_domain(self) -> Invoice:
        """
        Convert the serializer data to a domain model.
        
        Returns:
            A domain model instance.
        """
        validated_data = self.validated_data
        
        return Invoice(
            due_date=validated_data.get('due_date'),
            tax_amount=validated_data.get('tax_amount', 0),
            discount_amount=validated_data.get('discount_amount', 0),
            customer_name=validated_data.get('customer_name'),
            customer_email=validated_data.get('customer_email'),
            customer_phone=validated_data.get('customer_phone'),
            customer_address=validated_data.get('customer_address'),
            notes=validated_data.get('notes'),
            is_paid=validated_data.get('is_paid', False)
        )

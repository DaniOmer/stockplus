from rest_framework import serializers

from stockplus.modules.pointofsale.domain.entities import PosPaymentMethod


class PaymentMethodSerializer(serializers.Serializer):
    """
    Serializer for payment methods.
    """
    id = serializers.IntegerField(read_only=True)
    uid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    point_of_sale_id = serializers.IntegerField()
    is_active = serializers.BooleanField(default=True)
    requires_confirmation = serializers.BooleanField(default=False)
    confirmation_instructions = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    def to_domain(self) -> PosPaymentMethod:
        """
        Convert the serializer data to a domain model.
        
        Returns:
            The domain model.
        """
        return PosPaymentMethod(
            id=self.validated_data.get('id'),
            name=self.validated_data.get('name'),
            description=self.validated_data.get('description'),
            point_of_sale_id=self.validated_data.get('point_of_sale_id'),
            is_active=self.validated_data.get('is_active', True),
            requires_confirmation=self.validated_data.get('requires_confirmation', False),
            confirmation_instructions=self.validated_data.get('confirmation_instructions')
        )
    
    @classmethod
    def from_domain(cls, payment_method: PosPaymentMethod) -> dict:
        """
        Convert a domain model to serializer data.
        
        Args:
            payment_method: The domain model to convert.
            
        Returns:
            The serializer data.
        """
        return {
            'id': payment_method.id,
            'uid': payment_method.uid,
            'name': payment_method.name,
            'description': payment_method.description,
            'point_of_sale_id': payment_method.point_of_sale_id,
            'is_active': payment_method.is_active,
            'requires_confirmation': payment_method.requires_confirmation,
            'confirmation_instructions': payment_method.confirmation_instructions
        }

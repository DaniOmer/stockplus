from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from stockplus.modules.product.domain.entities import Brand
from stockplus.infrastructure.models import Brand as BrandORM


class BrandSerializer(serializers.Serializer):
    """
    Serializer for the brand model.
    """
    class Meta:
        model = BrandORM
        fields = ['id', 'uid', 'name', 'description', 'logo_url']
        read_only_fields = ['id', 'uid']

    def to_domain(self) -> Brand:
        """
        Convert the serializer data to a domain model.
        
        Returns:
            A domain model instance.
        """
        validated_data = self.validated_data
        
        return Brand(
            name=validated_data.get('name', ''),
            description=validated_data.get('description'),
            logo_url=validated_data.get('logo_url')
        )
    
    def create(self, validated_data):
        """
        Create a new brand.
        
        Args:
            validated_data: The validated data.
            
        Returns:
            The created brand.
            
        Raises:
            ValidationError: If the user does not have a company.
        """
        request = self.context.get('request')
        company = request.user.company

        if not company:
            raise ValidationError('You must provide your company information to continue.')
        
        validated_data['company'] = company
        return super().create(validated_data)

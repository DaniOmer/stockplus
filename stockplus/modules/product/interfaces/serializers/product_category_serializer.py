from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from stockplus.modules.product.domain.entities import ProductCategory
from stockplus.modules.product.infrastructure.models import ProductCategory as ProductCategoryORM


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the product category model.
    """
    class Meta:
        model = ProductCategoryORM
        fields = ['id', 'uid', 'name', 'description', 'parent']
        read_only_fields = ['id', 'uid']

    def to_domain(self) -> ProductCategory:
        """
        Convert the serializer data to a domain model.
        
        Returns:
            A domain model instance.
        """
        validated_data = self.validated_data
        
        return ProductCategory(
            name=validated_data.get('name', ''),
            description=validated_data.get('description'),
            parent_id=validated_data.get('parent_id')
        )
    
    def create(self, validated_data):
        """
        Create a new product category.
        
        Args:
            validated_data: The validated data.
            
        Returns:
            The created product category.
            
        Raises:
            ValidationError: If the user does not have a company.
        """
        request = self.context.get('request')
        company = request.user.company

        if not company:
            raise ValidationError('You must provide your company information to continue.')
        
        validated_data['company'] = company
        return super().create(validated_data)

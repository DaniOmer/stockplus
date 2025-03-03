from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from stockplus.modules.product.domain.entities import (
    Product, ProductFeature, ProductVariant
)
from stockplus.infrastructure.models import (
    Product as ProductORM,
    ProductFeature as ProductFeatureORM,
    ProductVariant as ProductVariantORM,
)

class ProductFeatureSerializer(serializers.ModelSerializer):
    """
    Serializer for the product feature model.
    """
    class Meta:
        model = ProductFeatureORM
        fields = ['id', 'uid', 'name', 'description']
        read_only_fields = ['id', 'uid']

    def to_domain(self) -> ProductFeature:
        """
        Convert the serializer data to a domain model.
        
        Returns:
            A domain model instance.
        """
        validated_data = self.validated_data
        
        return ProductFeature(
            name=validated_data.get('name', ''),
            description=validated_data.get('description')
        )



class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Serializer for the product variant model.
    """
    
    class Meta:
        model = ProductVariantORM
        fields = ['id', 'uid', 'name', 'color', 'size', 'price', 'buy_price', 'sku']
        read_only_fields = ['id', 'uid']

    def to_domain(self) -> ProductVariant:
        """
        Convert the serializer data to a domain model.
        
        Returns:
            A domain model instance.
        """
        validated_data = self.validated_data
        
        return ProductVariant(
            name=validated_data.get('name'),
            color=validated_data.get('color'),
            size=validated_data.get('size'),
            price=validated_data.get('price', 0.0),
            buy_price=validated_data.get('buy_price'),
            sku=validated_data.get('sku')
        )


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the product model.
    """
    features = ProductFeatureSerializer(many=True, required=False)
    variants = ProductVariantSerializer(many=True, required=False)
    
    class Meta:
        model = ProductORM
        fields = ['id', 'uid', 'name', 'description', 'brand', 'category', 'features', 'variants']
        read_only_fields = ['id', 'uid']

    def to_domain(self) -> Product:
        """
        Convert the serializer data to a domain model.
        
        Returns:
            A domain model instance.
        """
        validated_data = self.validated_data
        
        # Convert features
        features = []
        if 'features' in validated_data:
            for feature_data in validated_data['features']:
                feature_serializer = ProductFeatureSerializer(data=feature_data)
                feature_serializer.is_valid(raise_exception=True)
                features.append(feature_serializer.to_domain())
        
        # Convert variants
        variants = []
        if 'variants' in validated_data:
            for variant_data in validated_data['variants']:
                variant_serializer = ProductVariantSerializer(data=variant_data)
                variant_serializer.is_valid(raise_exception=True)
                variants.append(variant_serializer.to_domain())
        
        return Product(
            name=validated_data.get('name', ''),
            description=validated_data.get('description'),
            brand_id=validated_data.get('brand').id if 'brand' in validated_data else None,
            category_id=validated_data.get('category').id if 'category' in validated_data else None,
            features=features,
            variants=variants
        )
    
    def create(self, validated_data):
        """
        Create a new product.
        
        Args:
            validated_data: The validated data.
            
        Returns:
            The created product.
            
        Raises:
            ValidationError: If the user does not have a company.
        """
        request = self.context.get('request')
        company = request.user.company

        if not company:
            raise ValidationError('You must provide your company information to continue.')
        
        # Extract nested data
        features_data = validated_data.pop('features', [])
        variants_data = validated_data.pop('variants', [])
        
        # Create product
        validated_data['company'] = company
        product = super().create(validated_data)
        
        # Create features
        for feature_data in features_data:
            ProductFeatureORM.objects.create(product=product, **feature_data)
        
        # Create variants
        for variant_data in variants_data:
            point_of_sale_variants_data = variant_data.pop('point_of_sale_variants', [])
            variant = ProductVariantORM.objects.create(product=product, **variant_data)

        
        return product
    
    def update(self, instance, validated_data):
        """
        Update an existing product.
        
        Args:
            instance: The product instance to update.
            validated_data: The validated data.
            
        Returns:
            The updated product.
        """
        # Extract nested data
        features_data = validated_data.pop('features', [])
        variants_data = validated_data.pop('variants', [])
        
        # Update product
        instance = super().update(instance, validated_data)
        
        # Update features
        if features_data:
            # Delete existing features
            instance.features.all().delete()
            
            # Create new features
            for feature_data in features_data:
                ProductFeatureORM.objects.create(product=instance, **feature_data)
        
        # Update variants
        if variants_data:
            # Delete existing variants
            instance.variants.all().delete()
            
            # Create new variants
            for variant_data in variants_data:
                point_of_sale_variants_data = variant_data.pop('point_of_sale_variants', [])
                variant = ProductVariantORM.objects.create(product=instance, **variant_data)
                
        return instance

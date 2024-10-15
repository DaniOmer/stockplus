from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from stockplus.models import (
    Brand, Product, ProductCategory,
    ProductFeature, ProductVariant, PointOfSaleProductVariant
)

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'logo_url']

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'description']

class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['id', 'name', 'description']

class PointOfSaleProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfSaleProductVariant
        fields = ['id', 'point_of_sale', 'stock', 'price']

class ProductVariantSerializer(serializers.ModelSerializer):
    stocks = PointOfSaleProductVariantSerializer(many=True)
    class Meta:
        model = ProductVariant
        fields = ['id', 'color', 'size', 'price', 'buy_price', 'sku', 'stocks']

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'brand', 'category', 'variants']
    
    def create(self, validated_data):
        request = self.context.get('request')
        company = request.user.company

        if not company:
            raise ValidationError('You must provide your company information to continue.')
        
        variants_data = validated_data.pop('variants', [])
        product = Product.objects.create(company=company, **validated_data)
        for variant_data in variants_data:
            product_variant = ProductVariantSerializer.objects.create(product=product, **variant_data)
            for stock_data in variant_data['stocks']:
                PointOfSaleProductVariantSerializer.objects.create(product_variant=product_variant, **stock_data)
        return product
from decimal import Decimal
from typing import List, Optional

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from stockplus.modules.product.domain.entities import (
    Product as ProductDomain,
    ProductFeature as ProductFeatureDomain,
    ProductVariant as ProductVariantDomain,
)
from stockplus.modules.product.domain.exceptions import (
    ProductNotFoundError, ProductFeatureNotFoundError,
    ProductVariantNotFoundError
)
from stockplus.modules.product.application.interfaces import IProductRepository
from stockplus.modules.product.infrastructure.models import (
    Product as ProductORM,
    ProductFeature as ProductFeatureORM,
    ProductVariant as ProductVariantORM,
)

class ProductRepository(IProductRepository):
    """
    Django implementation of the product repository.
    """
    
    def _to_domain_feature(self, orm_feature: ProductORM) -> ProductFeatureDomain:
        """
        Convert an ORM product feature to a domain product feature.
        
        Args:
            orm_feature: The ORM product feature to convert.
            
        Returns:
            The domain product feature.
        """
        return ProductFeatureDomain(
            id=orm_feature.id,
            uid=orm_feature.uid,
            name=orm_feature.name,
            description=orm_feature.description,
            product_id=orm_feature.product_id,
            is_active=not orm_feature.is_disable
        )
    
    def _to_domain_variant(self, orm_variant: ProductVariantORM) -> ProductVariantDomain:
        """
        Convert an ORM product variant to a domain product variant.
        
        Args:
            orm_variant: The ORM product variant to convert.
            
        Returns:
            The domain product variant.
        """
        return ProductVariantDomain(
            id=orm_variant.id,
            uid=orm_variant.uid,
            name=orm_variant.name,
            product_id=orm_variant.product_id,
            color=orm_variant.color,
            size=orm_variant.size,
            price=float(orm_variant.price),
            buy_price=float(orm_variant.buy_price) if orm_variant.buy_price else None,
            sku=orm_variant.sku,
            is_active=not orm_variant.is_disable
        )
    
    def _to_domain(self, orm_product: ProductORM) -> ProductDomain:
        """
        Convert an ORM product to a domain product.
        
        Args:
            orm_product: The ORM product to convert.
            
        Returns:
            The domain product.
        """
        # Get features
        orm_features = orm_product.features.all()
        features = [self._to_domain_feature(feature) for feature in orm_features]
        
        # Get variants
        orm_variants = orm_product.variants.all()
        variants = [self._to_domain_variant(variant) for variant in orm_variants]
        
        return ProductDomain(
            id=orm_product.id,
            uid=orm_product.uid,
            name=orm_product.name,
            description=orm_product.description,
            brand_id=orm_product.brand_id,
            category_id=orm_product.category_id,
            company_id=orm_product.company_id,
            features=features,
            variants=variants,
            is_active=not orm_product.is_disable
        )
    
    def get_by_id(self, product_id: int) -> Optional[ProductDomain]:
        """
        Get a product by its ID.
        
        Args:
            product_id: The ID of the product to retrieve.
            
        Returns:
            The product if found, None otherwise.
        """
        try:
            orm_product = ProductORM.objects.get(id=product_id)
            return self._to_domain(orm_product)
        except ObjectDoesNotExist:
            return None
    
    def get_by_company_id(self, company_id: int) -> List[ProductDomain]:
        """
        Get all products for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of products for the company.
        """
        orm_products = ProductORM.objects.filter(company_id=company_id)
        return [self._to_domain(product) for product in orm_products]
    
    @transaction.atomic
    def create(self, product: ProductDomain) -> ProductDomain:
        """
        Create a new product.
        
        Args:
            product: The product to create.
            
        Returns:
            The created product.
        """
        orm_product = ProductORM.objects.create(
            name=product.name,
            description=product.description,
            brand_id=product.brand_id,
            category_id=product.category_id,
            company_id=product.company_id,
            is_disable=not product.is_active
        )
        
        # Create features
        for feature in product.features:
            self.add_feature(orm_product.id, feature)
        
        # Create variants
        for variant in product.variants:
            self.add_variant(orm_product.id, variant)
        
        return self._to_domain(orm_product)
    
    @transaction.atomic
    def update(self, product: ProductDomain) -> ProductDomain:
        """
        Update an existing product.
        
        Args:
            product: The product to update.
            
        Returns:
            The updated product.
            
        Raises:
            ProductNotFoundError: If the product is not found.
        """
        try:
            orm_product = ProductORM.objects.get(id=product.id)
        except ObjectDoesNotExist:
            raise ProductNotFoundError(product.id)
        
        orm_product.name = product.name
        orm_product.description = product.description
        orm_product.brand_id = product.brand_id
        orm_product.category_id = product.category_id
        orm_product.is_disable = not product.is_active
        orm_product.save()
        
        return self._to_domain(orm_product)
    
    def delete(self, product_id: int) -> None:
        """
        Delete a product.
        
        Args:
            product_id: The ID of the product to delete.
            
        Raises:
            ProductNotFoundError: If the product is not found.
        """
        try:
            orm_product = ProductORM.objects.get(id=product_id)
            orm_product.delete()
        except ObjectDoesNotExist:
            raise ProductNotFoundError(product_id)
    
    @transaction.atomic
    def add_feature(self, product_id: int, feature: ProductFeatureDomain) -> ProductFeatureDomain:
        """
        Add a feature to a product.
        
        Args:
            product_id: The ID of the product.
            feature: The feature to add.
            
        Returns:
            The added feature.
            
        Raises:
            ProductNotFoundError: If the product is not found.
        """
        try:
            ProductORM.objects.get(id=product_id)
        except ObjectDoesNotExist:
            raise ProductNotFoundError(product_id)
        
        orm_feature = ProductFeatureORM.objects.create(
            name=feature.name,
            description=feature.description,
            product_id=product_id,
            is_disable=not feature.is_active
        )
        
        return self._to_domain_feature(orm_feature)
    
    @transaction.atomic
    def update_feature(self, feature: ProductFeatureDomain) -> ProductFeatureDomain:
        """
        Update a product feature.
        
        Args:
            feature: The feature to update.
            
        Returns:
            The updated feature.
            
        Raises:
            ProductFeatureNotFoundError: If the feature is not found.
        """
        try:
            orm_feature = ProductFeatureORM.objects.get(id=feature.id)
        except ObjectDoesNotExist:
            raise ProductFeatureNotFoundError(feature.id)
        
        orm_feature.name = feature.name
        orm_feature.description = feature.description
        orm_feature.is_disable = not feature.is_active
        orm_feature.save()
        
        return self._to_domain_feature(orm_feature)
    
    def delete_feature(self, feature_id: int) -> None:
        """
        Delete a product feature.
        
        Args:
            feature_id: The ID of the feature to delete.
            
        Raises:
            ProductFeatureNotFoundError: If the feature is not found.
        """
        try:
            orm_feature = ProductFeatureORM.objects.get(id=feature_id)
            orm_feature.delete()
        except ObjectDoesNotExist:
            raise ProductFeatureNotFoundError(feature_id)
    
    @transaction.atomic
    def add_variant(self, product_id: int, variant: ProductVariantDomain) -> ProductVariantDomain:
        """
        Add a variant to a product.
        
        Args:
            product_id: The ID of the product.
            variant: The variant to add.
            
        Returns:
            The added variant.
            
        Raises:
            ProductNotFoundError: If the product is not found.
        """
        try:
            ProductORM.objects.get(id=product_id)
        except ObjectDoesNotExist:
            raise ProductNotFoundError(product_id)
        
        orm_variant = ProductVariantORM.objects.create(
            name=variant.name,
            product_id=product_id,
            color=variant.color,
            size=variant.size,
            price=Decimal(str(variant.price)),
            buy_price=Decimal(str(variant.buy_price)) if variant.buy_price is not None else None,
            sku=variant.sku,
            is_disable=not variant.is_active
        )
        
        return self._to_domain_variant(orm_variant)
    
    @transaction.atomic
    def update_variant(self, variant: ProductVariantDomain) -> ProductVariantDomain:
        """
        Update a product variant.
        
        Args:
            variant: The variant to update.
            
        Returns:
            The updated variant.
            
        Raises:
            ProductVariantNotFoundError: If the variant is not found.
        """
        try:
            orm_variant = ProductVariantORM.objects.get(id=variant.id)
        except ObjectDoesNotExist:
            raise ProductVariantNotFoundError(variant.id)
        
        orm_variant.name = variant.name
        orm_variant.color = variant.color
        orm_variant.size = variant.size
        orm_variant.price = Decimal(str(variant.price))
        orm_variant.buy_price = Decimal(str(variant.buy_price)) if variant.buy_price is not None else None
        orm_variant.sku = variant.sku
        orm_variant.is_disable = not variant.is_active
        orm_variant.save()
        
        return self._to_domain_variant(orm_variant)
    
    def delete_variant(self, variant_id: int) -> None:
        """
        Delete a product variant.
        
        Args:
            variant_id: The ID of the variant to delete.
            
        Raises:
            ProductVariantNotFoundError: If the variant is not found.
        """
        try:
            orm_variant = ProductVariantORM.objects.get(id=variant_id)
            orm_variant.delete()
        except ObjectDoesNotExist:
            raise ProductVariantNotFoundError(variant_id)

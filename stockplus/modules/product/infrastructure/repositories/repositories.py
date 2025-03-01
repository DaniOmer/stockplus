from decimal import Decimal
from typing import List, Optional

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from stockplus.modules.product.application.interfaces import (
    BrandRepository, ProductCategoryRepository, 
    ProductRepository, PointOfSaleProductVariantRepository
)
from stockplus.modules.product.domain.exceptions import (
    BrandNotFoundError, ProductCategoryNotFoundError, 
    ProductNotFoundError, ProductFeatureNotFoundError,
    ProductVariantNotFoundError, PointOfSaleProductVariantNotFoundError
)
from stockplus.modules.product.domain.models import (
    Brand as BrandDomain,
    Product as ProductDomain,
    ProductCategory as ProductCategoryDomain,
    ProductFeature as ProductFeatureDomain,
    ProductVariant as ProductVariantDomain,
    PointOfSaleProductVariant as PointOfSaleProductVariantDomain
)
from stockplus.modules.product.infrastructure.orm import (
    Brand as BrandORM,
    Product as ProductORM,
    ProductCategory as ProductCategoryORM,
    ProductFeature as ProductFeatureORM,
    ProductVariant as ProductVariantORM,
    PointOfSaleProductVariant as PointOfSaleProductVariantORM
)


class BrandRepository(BrandRepository):
    """
    Django implementation of the brand repository.
    """
    
    def _to_domain(self, orm_brand: BrandORM) -> BrandDomain:
        """
        Convert an ORM brand to a domain brand.
        
        Args:
            orm_brand: The ORM brand to convert.
            
        Returns:
            The domain brand.
        """
        return BrandDomain(
            id=orm_brand.id,
            uid=orm_brand.uid,
            name=orm_brand.name,
            description=orm_brand.description,
            logo_url=orm_brand.logo_url,
            company_id=orm_brand.company_id,
            is_active=not orm_brand.is_disable
        )
    
    def get_by_id(self, brand_id: int) -> Optional[BrandDomain]:
        """
        Get a brand by its ID.
        
        Args:
            brand_id: The ID of the brand to retrieve.
            
        Returns:
            The brand if found, None otherwise.
        """
        try:
            orm_brand = BrandORM.objects.get(id=brand_id)
            return self._to_domain(orm_brand)
        except ObjectDoesNotExist:
            return None
    
    def get_by_company_id(self, company_id: int) -> List[BrandDomain]:
        """
        Get all brands for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of brands for the company.
        """
        orm_brands = BrandORM.objects.filter(company_id=company_id)
        return [self._to_domain(brand) for brand in orm_brands]
    
    @transaction.atomic
    def create(self, brand: BrandDomain) -> BrandDomain:
        """
        Create a new brand.
        
        Args:
            brand: The brand to create.
            
        Returns:
            The created brand.
        """
        orm_brand = BrandORM.objects.create(
            name=brand.name,
            description=brand.description,
            logo_url=brand.logo_url,
            company_id=brand.company_id,
            is_disable=not brand.is_active
        )
        return self._to_domain(orm_brand)
    
    @transaction.atomic
    def update(self, brand: BrandDomain) -> BrandDomain:
        """
        Update an existing brand.
        
        Args:
            brand: The brand to update.
            
        Returns:
            The updated brand.
            
        Raises:
            BrandNotFoundError: If the brand is not found.
        """
        try:
            orm_brand = BrandORM.objects.get(id=brand.id)
        except ObjectDoesNotExist:
            raise BrandNotFoundError(brand.id)
        
        orm_brand.name = brand.name
        orm_brand.description = brand.description
        orm_brand.logo_url = brand.logo_url
        orm_brand.is_disable = not brand.is_active
        orm_brand.save()
        
        return self._to_domain(orm_brand)
    
    def delete(self, brand_id: int) -> None:
        """
        Delete a brand.
        
        Args:
            brand_id: The ID of the brand to delete.
            
        Raises:
            BrandNotFoundError: If the brand is not found.
        """
        try:
            orm_brand = BrandORM.objects.get(id=brand_id)
            orm_brand.delete()
        except ObjectDoesNotExist:
            raise BrandNotFoundError(brand_id)


class ProductCategoryRepository(ProductCategoryRepository):
    """
    Django implementation of the product category repository.
    """
    
    def _to_domain(self, orm_category: ProductCategoryORM) -> ProductCategoryDomain:
        """
        Convert an ORM product category to a domain product category.
        
        Args:
            orm_category: The ORM product category to convert.
            
        Returns:
            The domain product category.
        """
        return ProductCategoryDomain(
            id=orm_category.id,
            uid=orm_category.uid,
            name=orm_category.name,
            description=orm_category.description,
            parent_id=orm_category.parent_id,
            company_id=orm_category.company_id,
            is_active=not orm_category.is_disable
        )
    
    def get_by_id(self, category_id: int) -> Optional[ProductCategoryDomain]:
        """
        Get a product category by its ID.
        
        Args:
            category_id: The ID of the product category to retrieve.
            
        Returns:
            The product category if found, None otherwise.
        """
        try:
            orm_category = ProductCategoryORM.objects.get(id=category_id)
            return self._to_domain(orm_category)
        except ObjectDoesNotExist:
            return None
    
    def get_by_company_id(self, company_id: int) -> List[ProductCategoryDomain]:
        """
        Get all product categories for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of product categories for the company.
        """
        orm_categories = ProductCategoryORM.objects.filter(company_id=company_id)
        return [self._to_domain(category) for category in orm_categories]
    
    @transaction.atomic
    def create(self, category: ProductCategoryDomain) -> ProductCategoryDomain:
        """
        Create a new product category.
        
        Args:
            category: The product category to create.
            
        Returns:
            The created product category.
        """
        orm_category = ProductCategoryORM.objects.create(
            name=category.name,
            description=category.description,
            parent_id=category.parent_id,
            company_id=category.company_id,
            is_disable=not category.is_active
        )
        return self._to_domain(orm_category)
    
    @transaction.atomic
    def update(self, category: ProductCategoryDomain) -> ProductCategoryDomain:
        """
        Update an existing product category.
        
        Args:
            category: The product category to update.
            
        Returns:
            The updated product category.
            
        Raises:
            ProductCategoryNotFoundError: If the product category is not found.
        """
        try:
            orm_category = ProductCategoryORM.objects.get(id=category.id)
        except ObjectDoesNotExist:
            raise ProductCategoryNotFoundError(category.id)
        
        orm_category.name = category.name
        orm_category.description = category.description
        orm_category.parent_id = category.parent_id
        orm_category.is_disable = not category.is_active
        orm_category.save()
        
        return self._to_domain(orm_category)
    
    def delete(self, category_id: int) -> None:
        """
        Delete a product category.
        
        Args:
            category_id: The ID of the product category to delete.
            
        Raises:
            ProductCategoryNotFoundError: If the product category is not found.
        """
        try:
            orm_category = ProductCategoryORM.objects.get(id=category_id)
            orm_category.delete()
        except ObjectDoesNotExist:
            raise ProductCategoryNotFoundError(category_id)


class ProductRepository(ProductRepository):
    """
    Django implementation of the product repository.
    """
    
    def _to_domain_feature(self, orm_feature: ProductFeatureORM) -> ProductFeatureDomain:
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


class PointOfSaleProductVariantRepository(PointOfSaleProductVariantRepository):
    """
    Django implementation of the point of sale product variant repository.
    """
    
    def _to_domain(self, orm_pos_variant: PointOfSaleProductVariantORM) -> PointOfSaleProductVariantDomain:
        """
        Convert an ORM point of sale product variant to a domain point of sale product variant.
        
        Args:
            orm_pos_variant: The ORM point of sale product variant to convert.
            
        Returns:
            The domain point of sale product variant.
        """
        return PointOfSaleProductVariantDomain(
            id=orm_pos_variant.id,
            uid=orm_pos_variant.uid,
            point_of_sale_id=orm_pos_variant.point_of_sale_id,
            product_variant_id=orm_pos_variant.product_variant_id,
            stock=orm_pos_variant.stock,
            price=float(orm_pos_variant.price) if orm_pos_variant.price else None,
            is_active=not orm_pos_variant.is_disable
        )
    
    def get_by_id(self, pos_variant_id: int) -> Optional[PointOfSaleProductVariantDomain]:
        """
        Get a point of sale product variant by its ID.
        
        Args:
            pos_variant_id: The ID of the point of sale product variant to retrieve.
            
        Returns:
            The point of sale product variant if found, None otherwise.
        """
        try:
            orm_pos_variant = PointOfSaleProductVariantORM.objects.get(id=pos_variant_id)
            return self._to_domain(orm_pos_variant)
        except ObjectDoesNotExist:
            return None
    
    def get_by_point_of_sale_id(self, point_of_sale_id: int) -> List[PointOfSaleProductVariantDomain]:
        """
        Get all product variants for a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            
        Returns:
            A list of product variants for the point of sale.
        """
        orm_pos_variants = PointOfSaleProductVariantORM.objects.filter(point_of_sale_id=point_of_sale_id)
        return [self._to_domain(pos_variant) for pos_variant in orm_pos_variants]
    
    def get_by_product_variant_id(self, product_variant_id: int) -> List[PointOfSaleProductVariantDomain]:
        """
        Get all point of sale product variants for a product variant.
        
        Args:
            product_variant_id: The ID of the product variant.
            
        Returns:
            A list of point of sale product variants for the product variant.
        """
        orm_pos_variants = PointOfSaleProductVariantORM.objects.filter(product_variant_id=product_variant_id)
        return [self._to_domain(pos_variant) for pos_variant in orm_pos_variants]
    
    @transaction.atomic
    def create(self, pos_variant: PointOfSaleProductVariantDomain) -> PointOfSaleProductVariantDomain:
        """
        Create a new point of sale product variant.
        
        Args:
            pos_variant: The point of sale product variant to create.
            
        Returns:
            The created point of sale product variant.
        """
        orm_pos_variant = PointOfSaleProductVariantORM.objects.create(
            point_of_sale_id=pos_variant.point_of_sale_id,
            product_variant_id=pos_variant.product_variant_id,
            stock=pos_variant.stock,
            price=Decimal(str(pos_variant.price)) if pos_variant.price is not None else None,
            is_disable=not pos_variant.is_active
        )
        
        return self._to_domain(orm_pos_variant)
    
    @transaction.atomic
    def update(self, pos_variant: PointOfSaleProductVariantDomain) -> PointOfSaleProductVariantDomain:
        """
        Update an existing point of sale product variant.
        
        Args:
            pos_variant: The point of sale product variant to update.
            
        Returns:
            The updated point of sale product variant.
            
        Raises:
            PointOfSaleProductVariantNotFoundError: If the point of sale product variant is not found.
        """
        try:
            orm_pos_variant = PointOfSaleProductVariantORM.objects.get(id=pos_variant.id)
        except ObjectDoesNotExist:
            raise PointOfSaleProductVariantNotFoundError(pos_variant.id)
        
        orm_pos_variant.stock = pos_variant.stock
        orm_pos_variant.price = Decimal(str(pos_variant.price)) if pos_variant.price is not None else None
        orm_pos_variant.is_disable = not pos_variant.is_active
        orm_pos_variant.save()
        
        return self._to_domain(orm_pos_variant)
    
    def delete(self, pos_variant_id: int) -> None:
        """
        Delete a point of sale product variant.
        
        Args:
            pos_variant_id: The ID of the point of sale product variant to delete.
            
        Raises:
            PointOfSaleProductVariantNotFoundError: If the point of sale product variant is not found.
        """
        try:
            orm_pos_variant = PointOfSaleProductVariantORM.objects.get(id=pos_variant_id)
            orm_pos_variant.delete()
        except ObjectDoesNotExist:
            raise PointOfSaleProductVariantNotFoundError(pos_variant_id)

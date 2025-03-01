from abc import ABC, abstractmethod
from typing import List, Optional

from stockplus.modules.product.domain.models import (
    Brand, Product, ProductCategory, ProductFeature, 
    ProductVariant, PointOfSaleProductVariant
)


class BrandRepository(ABC):
    """
    Interface for the brand repository.
    """
    @abstractmethod
    def get_by_id(self, brand_id: int) -> Optional[Brand]:
        """
        Get a brand by its ID.
        
        Args:
            brand_id: The ID of the brand to retrieve.
            
        Returns:
            The brand if found, None otherwise.
        """
        pass
    
    @abstractmethod
    def get_by_company_id(self, company_id: int) -> List[Brand]:
        """
        Get all brands for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of brands for the company.
        """
        pass
    
    @abstractmethod
    def create(self, brand: Brand) -> Brand:
        """
        Create a new brand.
        
        Args:
            brand: The brand to create.
            
        Returns:
            The created brand.
        """
        pass
    
    @abstractmethod
    def update(self, brand: Brand) -> Brand:
        """
        Update an existing brand.
        
        Args:
            brand: The brand to update.
            
        Returns:
            The updated brand.
        """
        pass
    
    @abstractmethod
    def delete(self, brand_id: int) -> None:
        """
        Delete a brand.
        
        Args:
            brand_id: The ID of the brand to delete.
        """
        pass


class ProductCategoryRepository(ABC):
    """
    Interface for the product category repository.
    """
    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[ProductCategory]:
        """
        Get a product category by its ID.
        
        Args:
            category_id: The ID of the product category to retrieve.
            
        Returns:
            The product category if found, None otherwise.
        """
        pass
    
    @abstractmethod
    def get_by_company_id(self, company_id: int) -> List[ProductCategory]:
        """
        Get all product categories for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of product categories for the company.
        """
        pass
    
    @abstractmethod
    def create(self, category: ProductCategory) -> ProductCategory:
        """
        Create a new product category.
        
        Args:
            category: The product category to create.
            
        Returns:
            The created product category.
        """
        pass
    
    @abstractmethod
    def update(self, category: ProductCategory) -> ProductCategory:
        """
        Update an existing product category.
        
        Args:
            category: The product category to update.
            
        Returns:
            The updated product category.
        """
        pass
    
    @abstractmethod
    def delete(self, category_id: int) -> None:
        """
        Delete a product category.
        
        Args:
            category_id: The ID of the product category to delete.
        """
        pass


class ProductRepository(ABC):
    """
    Interface for the product repository.
    """
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Get a product by its ID.
        
        Args:
            product_id: The ID of the product to retrieve.
            
        Returns:
            The product if found, None otherwise.
        """
        pass
    
    @abstractmethod
    def get_by_company_id(self, company_id: int) -> List[Product]:
        """
        Get all products for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of products for the company.
        """
        pass
    
    @abstractmethod
    def create(self, product: Product) -> Product:
        """
        Create a new product.
        
        Args:
            product: The product to create.
            
        Returns:
            The created product.
        """
        pass
    
    @abstractmethod
    def update(self, product: Product) -> Product:
        """
        Update an existing product.
        
        Args:
            product: The product to update.
            
        Returns:
            The updated product.
        """
        pass
    
    @abstractmethod
    def delete(self, product_id: int) -> None:
        """
        Delete a product.
        
        Args:
            product_id: The ID of the product to delete.
        """
        pass
    
    @abstractmethod
    def add_feature(self, product_id: int, feature: ProductFeature) -> ProductFeature:
        """
        Add a feature to a product.
        
        Args:
            product_id: The ID of the product.
            feature: The feature to add.
            
        Returns:
            The added feature.
        """
        pass
    
    @abstractmethod
    def update_feature(self, feature: ProductFeature) -> ProductFeature:
        """
        Update a product feature.
        
        Args:
            feature: The feature to update.
            
        Returns:
            The updated feature.
        """
        pass
    
    @abstractmethod
    def delete_feature(self, feature_id: int) -> None:
        """
        Delete a product feature.
        
        Args:
            feature_id: The ID of the feature to delete.
        """
        pass
    
    @abstractmethod
    def add_variant(self, product_id: int, variant: ProductVariant) -> ProductVariant:
        """
        Add a variant to a product.
        
        Args:
            product_id: The ID of the product.
            variant: The variant to add.
            
        Returns:
            The added variant.
        """
        pass
    
    @abstractmethod
    def update_variant(self, variant: ProductVariant) -> ProductVariant:
        """
        Update a product variant.
        
        Args:
            variant: The variant to update.
            
        Returns:
            The updated variant.
        """
        pass
    
    @abstractmethod
    def delete_variant(self, variant_id: int) -> None:
        """
        Delete a product variant.
        
        Args:
            variant_id: The ID of the variant to delete.
        """
        pass


class PointOfSaleProductVariantRepository(ABC):
    """
    Interface for the point of sale product variant repository.
    """
    @abstractmethod
    def get_by_id(self, pos_variant_id: int) -> Optional[PointOfSaleProductVariant]:
        """
        Get a point of sale product variant by its ID.
        
        Args:
            pos_variant_id: The ID of the point of sale product variant to retrieve.
            
        Returns:
            The point of sale product variant if found, None otherwise.
        """
        pass
    
    @abstractmethod
    def get_by_point_of_sale_id(self, point_of_sale_id: int) -> List[PointOfSaleProductVariant]:
        """
        Get all product variants for a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            
        Returns:
            A list of product variants for the point of sale.
        """
        pass
    
    @abstractmethod
    def get_by_product_variant_id(self, product_variant_id: int) -> List[PointOfSaleProductVariant]:
        """
        Get all point of sale product variants for a product variant.
        
        Args:
            product_variant_id: The ID of the product variant.
            
        Returns:
            A list of point of sale product variants for the product variant.
        """
        pass
    
    @abstractmethod
    def create(self, pos_variant: PointOfSaleProductVariant) -> PointOfSaleProductVariant:
        """
        Create a new point of sale product variant.
        
        Args:
            pos_variant: The point of sale product variant to create.
            
        Returns:
            The created point of sale product variant.
        """
        pass
    
    @abstractmethod
    def update(self, pos_variant: PointOfSaleProductVariant) -> PointOfSaleProductVariant:
        """
        Update an existing point of sale product variant.
        
        Args:
            pos_variant: The point of sale product variant to update.
            
        Returns:
            The updated point of sale product variant.
        """
        pass
    
    @abstractmethod
    def delete(self, pos_variant_id: int) -> None:
        """
        Delete a point of sale product variant.
        
        Args:
            pos_variant_id: The ID of the point of sale product variant to delete.
        """
        pass

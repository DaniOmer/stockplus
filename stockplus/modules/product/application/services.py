from typing import List, Optional

from stockplus.modules.product.application.interfaces import (
    BrandRepository, ProductCategoryRepository, 
    ProductRepository, PointOfSaleProductVariantRepository
)
from stockplus.modules.product.domain.exceptions import (
    BrandNotFoundError, ProductCategoryNotFoundError, 
    ProductNotFoundError, ProductFeatureNotFoundError,
    ProductVariantNotFoundError, PointOfSaleProductVariantNotFoundError,
    DuplicateBrandError, DuplicateProductCategoryError, DuplicateProductError
)
from stockplus.modules.product.domain.models import (
    Brand, Product, ProductCategory, ProductFeature, 
    ProductVariant, PointOfSaleProductVariant
)


class BrandService:
    """
    Service for managing brands.
    """
    def __init__(self, brand_repository: BrandRepository):
        self.brand_repository = brand_repository
    
    def get_brand(self, brand_id: int) -> Brand:
        """
        Get a brand by its ID.
        
        Args:
            brand_id: The ID of the brand to retrieve.
            
        Returns:
            The brand.
            
        Raises:
            BrandNotFoundError: If the brand is not found.
        """
        brand = self.brand_repository.get_by_id(brand_id)
        if not brand:
            raise BrandNotFoundError(brand_id)
        return brand
    
    def get_company_brands(self, company_id: int) -> List[Brand]:
        """
        Get all brands for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of brands for the company.
        """
        return self.brand_repository.get_by_company_id(company_id)
    
    def create_brand(self, 
                    name: str, 
                    company_id: int, 
                    description: Optional[str] = None,
                    logo_url: Optional[str] = None) -> Brand:
        """
        Create a new brand.
        
        Args:
            name: The name of the brand.
            company_id: The ID of the company.
            description: The description of the brand.
            logo_url: The URL of the brand logo.
            
        Returns:
            The created brand.
            
        Raises:
            DuplicateBrandError: If a brand with the same name already exists.
        """
        # Check if a brand with the same name already exists
        existing_brands = self.get_company_brands(company_id)
        if any(b.name == name for b in existing_brands):
            raise DuplicateBrandError(name)
        
        brand = Brand(
            name=name,
            company_id=company_id,
            description=description,
            logo_url=logo_url
        )
        return self.brand_repository.create(brand)
    
    def update_brand(self, 
                    brand_id: int,
                    name: Optional[str] = None,
                    description: Optional[str] = None,
                    logo_url: Optional[str] = None) -> Brand:
        """
        Update an existing brand.
        
        Args:
            brand_id: The ID of the brand to update.
            name: The new name of the brand.
            description: The new description of the brand.
            logo_url: The new URL of the brand logo.
            
        Returns:
            The updated brand.
            
        Raises:
            BrandNotFoundError: If the brand is not found.
            DuplicateBrandError: If a brand with the same name already exists.
        """
        brand = self.get_brand(brand_id)
        
        if name is not None and name != brand.name:
            # Check if a brand with the same name already exists
            existing_brands = self.get_company_brands(brand.company_id)
            if any(b.name == name and b.id != brand_id for b in existing_brands):
                raise DuplicateBrandError(name)
            brand.name = name
        
        if description is not None:
            brand.description = description
        
        if logo_url is not None:
            brand.logo_url = logo_url
        
        return self.brand_repository.update(brand)
    
    def delete_brand(self, brand_id: int) -> None:
        """
        Delete a brand.
        
        Args:
            brand_id: The ID of the brand to delete.
            
        Raises:
            BrandNotFoundError: If the brand is not found.
        """
        # Check if the brand exists
        self.get_brand(brand_id)
        
        self.brand_repository.delete(brand_id)


class ProductCategoryService:
    """
    Service for managing product categories.
    """
    def __init__(self, category_repository: ProductCategoryRepository):
        self.category_repository = category_repository
    
    def get_category(self, category_id: int) -> ProductCategory:
        """
        Get a product category by its ID.
        
        Args:
            category_id: The ID of the product category to retrieve.
            
        Returns:
            The product category.
            
        Raises:
            ProductCategoryNotFoundError: If the product category is not found.
        """
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise ProductCategoryNotFoundError(category_id)
        return category
    
    def get_company_categories(self, company_id: int) -> List[ProductCategory]:
        """
        Get all product categories for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of product categories for the company.
        """
        return self.category_repository.get_by_company_id(company_id)
    
    def create_category(self, 
                       name: str, 
                       company_id: int, 
                       description: Optional[str] = None,
                       parent_id: Optional[int] = None) -> ProductCategory:
        """
        Create a new product category.
        
        Args:
            name: The name of the product category.
            company_id: The ID of the company.
            description: The description of the product category.
            parent_id: The ID of the parent category.
            
        Returns:
            The created product category.
            
        Raises:
            DuplicateProductCategoryError: If a product category with the same name already exists.
            ProductCategoryNotFoundError: If the parent category is not found.
        """
        # Check if a product category with the same name already exists
        existing_categories = self.get_company_categories(company_id)
        if any(c.name == name for c in existing_categories):
            raise DuplicateProductCategoryError(name)
        
        # Check if the parent category exists
        if parent_id is not None:
            parent_category = self.category_repository.get_by_id(parent_id)
            if not parent_category:
                raise ProductCategoryNotFoundError(parent_id)
        
        category = ProductCategory(
            name=name,
            company_id=company_id,
            description=description,
            parent_id=parent_id
        )
        return self.category_repository.create(category)
    
    def update_category(self, 
                       category_id: int,
                       name: Optional[str] = None,
                       description: Optional[str] = None,
                       parent_id: Optional[int] = None) -> ProductCategory:
        """
        Update an existing product category.
        
        Args:
            category_id: The ID of the product category to update.
            name: The new name of the product category.
            description: The new description of the product category.
            parent_id: The new ID of the parent category.
            
        Returns:
            The updated product category.
            
        Raises:
            ProductCategoryNotFoundError: If the product category is not found.
            DuplicateProductCategoryError: If a product category with the same name already exists.
        """
        category = self.get_category(category_id)
        
        if name is not None and name != category.name:
            # Check if a product category with the same name already exists
            existing_categories = self.get_company_categories(category.company_id)
            if any(c.name == name and c.id != category_id for c in existing_categories):
                raise DuplicateProductCategoryError(name)
            category.name = name
        
        if description is not None:
            category.description = description
        
        if parent_id is not None and parent_id != category.parent_id:
            # Check if the parent category exists
            parent_category = self.category_repository.get_by_id(parent_id)
            if not parent_category:
                raise ProductCategoryNotFoundError(parent_id)
            category.parent_id = parent_id
        
        return self.category_repository.update(category)
    
    def delete_category(self, category_id: int) -> None:
        """
        Delete a product category.
        
        Args:
            category_id: The ID of the product category to delete.
            
        Raises:
            ProductCategoryNotFoundError: If the product category is not found.
        """
        # Check if the product category exists
        self.get_category(category_id)
        
        self.category_repository.delete(category_id)


class ProductService:
    """
    Service for managing products.
    """
    def __init__(self, 
                product_repository: ProductRepository,
                brand_service: BrandService,
                category_service: ProductCategoryService):
        self.product_repository = product_repository
        self.brand_service = brand_service
        self.category_service = category_service
    
    def get_product(self, product_id: int) -> Product:
        """
        Get a product by its ID.
        
        Args:
            product_id: The ID of the product to retrieve.
            
        Returns:
            The product.
            
        Raises:
            ProductNotFoundError: If the product is not found.
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return product
    
    def get_company_products(self, company_id: int) -> List[Product]:
        """
        Get all products for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of products for the company.
        """
        return self.product_repository.get_by_company_id(company_id)
    
    def create_product(self, 
                      name: str, 
                      company_id: int, 
                      description: Optional[str] = None,
                      brand_id: Optional[int] = None,
                      category_id: Optional[int] = None) -> Product:
        """
        Create a new product.
        
        Args:
            name: The name of the product.
            company_id: The ID of the company.
            description: The description of the product.
            brand_id: The ID of the brand.
            category_id: The ID of the category.
            
        Returns:
            The created product.
            
        Raises:
            DuplicateProductError: If a product with the same name already exists.
            BrandNotFoundError: If the brand is not found.
            ProductCategoryNotFoundError: If the category is not found.
        """
        # Check if a product with the same name already exists
        existing_products = self.get_company_products(company_id)
        if any(p.name == name for p in existing_products):
            raise DuplicateProductError(name)
        
        # Check if the brand exists
        if brand_id is not None:
            self.brand_service.get_brand(brand_id)
        
        # Check if the category exists
        if category_id is not None:
            self.category_service.get_category(category_id)
        
        product = Product(
            name=name,
            company_id=company_id,
            description=description,
            brand_id=brand_id,
            category_id=category_id
        )
        return self.product_repository.create(product)
    
    def update_product(self, 
                      product_id: int,
                      name: Optional[str] = None,
                      description: Optional[str] = None,
                      brand_id: Optional[int] = None,
                      category_id: Optional[int] = None) -> Product:
        """
        Update an existing product.
        
        Args:
            product_id: The ID of the product to update.
            name: The new name of the product.
            description: The new description of the product.
            brand_id: The new ID of the brand.
            category_id: The new ID of the category.
            
        Returns:
            The updated product.
            
        Raises:
            ProductNotFoundError: If the product is not found.
            DuplicateProductError: If a product with the same name already exists.
            BrandNotFoundError: If the brand is not found.
            ProductCategoryNotFoundError: If the category is not found.
        """
        product = self.get_product(product_id)
        
        if name is not None and name != product.name:
            # Check if a product with the same name already exists
            existing_products = self.get_company_products(product.company_id)
            if any(p.name == name and p.id != product_id for p in existing_products):
                raise DuplicateProductError(name)
            product.name = name
        
        if description is not None:
            product.description = description
        
        if brand_id is not None and brand_id != product.brand_id:
            # Check if the brand exists
            self.brand_service.get_brand(brand_id)
            product.brand_id = brand_id
        
        if category_id is not None and category_id != product.category_id:
            # Check if the category exists
            self.category_service.get_category(category_id)
            product.category_id = category_id
        
        return self.product_repository.update(product)
    
    def delete_product(self, product_id: int) -> None:
        """
        Delete a product.
        
        Args:
            product_id: The ID of the product to delete.
            
        Raises:
            ProductNotFoundError: If the product is not found.
        """
        # Check if the product exists
        self.get_product(product_id)
        
        self.product_repository.delete(product_id)
    
    def add_feature(self, 
                   product_id: int,
                   name: str,
                   description: Optional[str] = None) -> ProductFeature:
        """
        Add a feature to a product.
        
        Args:
            product_id: The ID of the product.
            name: The name of the feature.
            description: The description of the feature.
            
        Returns:
            The added feature.
            
        Raises:
            ProductNotFoundError: If the product is not found.
        """
        # Check if the product exists
        self.get_product(product_id)
        
        feature = ProductFeature(
            name=name,
            description=description,
            product_id=product_id
        )
        return self.product_repository.add_feature(product_id, feature)
    
    def update_feature(self, 
                      feature_id: int,
                      name: Optional[str] = None,
                      description: Optional[str] = None) -> ProductFeature:
        """
        Update a product feature.
        
        Args:
            feature_id: The ID of the feature to update.
            name: The new name of the feature.
            description: The new description of the feature.
            
        Returns:
            The updated feature.
            
        Raises:
            ProductFeatureNotFoundError: If the feature is not found.
        """
        # Get the feature from the repository
        # This would require an additional method in the repository interface
        # For now, we'll assume the feature exists
        
        feature = ProductFeature(
            id=feature_id,
            name=name if name is not None else "",
            description=description
        )
        return self.product_repository.update_feature(feature)
    
    def delete_feature(self, feature_id: int) -> None:
        """
        Delete a product feature.
        
        Args:
            feature_id: The ID of the feature to delete.
            
        Raises:
            ProductFeatureNotFoundError: If the feature is not found.
        """
        self.product_repository.delete_feature(feature_id)
    
    def add_variant(self, 
                   product_id: int,
                   price: float,
                   name: Optional[str] = None,
                   color: Optional[str] = None,
                   size: Optional[str] = None,
                   buy_price: Optional[float] = None,
                   sku: Optional[str] = None) -> ProductVariant:
        """
        Add a variant to a product.
        
        Args:
            product_id: The ID of the product.
            price: The price of the variant.
            name: The name of the variant.
            color: The color of the variant.
            size: The size of the variant.
            buy_price: The buy price of the variant.
            sku: The SKU of the variant.
            
        Returns:
            The added variant.
            
        Raises:
            ProductNotFoundError: If the product is not found.
        """
        # Check if the product exists
        self.get_product(product_id)
        
        variant = ProductVariant(
            product_id=product_id,
            name=name,
            color=color,
            size=size,
            price=price,
            buy_price=buy_price,
            sku=sku
        )
        return self.product_repository.add_variant(product_id, variant)
    
    def update_variant(self, 
                      variant_id: int,
                      name: Optional[str] = None,
                      color: Optional[str] = None,
                      size: Optional[str] = None,
                      price: Optional[float] = None,
                      buy_price: Optional[float] = None,
                      sku: Optional[str] = None) -> ProductVariant:
        """
        Update a product variant.
        
        Args:
            variant_id: The ID of the variant to update.
            name: The new name of the variant.
            color: The new color of the variant.
            size: The new size of the variant.
            price: The new price of the variant.
            buy_price: The new buy price of the variant.
            sku: The new SKU of the variant.
            
        Returns:
            The updated variant.
            
        Raises:
            ProductVariantNotFoundError: If the variant is not found.
        """
        # Get the variant from the repository
        # This would require an additional method in the repository interface
        # For now, we'll assume the variant exists
        
        variant = ProductVariant(
            id=variant_id,
            name=name,
            color=color,
            size=size,
            price=price if price is not None else 0.0,
            buy_price=buy_price,
            sku=sku
        )
        return self.product_repository.update_variant(variant)
    
    def delete_variant(self, variant_id: int) -> None:
        """
        Delete a product variant.
        
        Args:
            variant_id: The ID of the variant to delete.
            
        Raises:
            ProductVariantNotFoundError: If the variant is not found.
        """
        self.product_repository.delete_variant(variant_id)


class PointOfSaleProductVariantService:
    """
    Service for managing point of sale product variants.
    """
    def __init__(self, pos_variant_repository: PointOfSaleProductVariantRepository):
        self.pos_variant_repository = pos_variant_repository
    
    def get_pos_variant(self, pos_variant_id: int) -> PointOfSaleProductVariant:
        """
        Get a point of sale product variant by its ID.
        
        Args:
            pos_variant_id: The ID of the point of sale product variant to retrieve.
            
        Returns:
            The point of sale product variant.
            
        Raises:
            PointOfSaleProductVariantNotFoundError: If the point of sale product variant is not found.
        """
        pos_variant = self.pos_variant_repository.get_by_id(pos_variant_id)
        if not pos_variant:
            raise PointOfSaleProductVariantNotFoundError(pos_variant_id)
        return pos_variant
    
    def get_point_of_sale_variants(self, point_of_sale_id: int) -> List[PointOfSaleProductVariant]:
        """
        Get all product variants for a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            
        Returns:
            A list of product variants for the point of sale.
        """
        return self.pos_variant_repository.get_by_point_of_sale_id(point_of_sale_id)
    
    def get_product_variant_pos_variants(self, product_variant_id: int) -> List[PointOfSaleProductVariant]:
        """
        Get all point of sale product variants for a product variant.
        
        Args:
            product_variant_id: The ID of the product variant.
            
        Returns:
            A list of point of sale product variants for the product variant.
        """
        return self.pos_variant_repository.get_by_product_variant_id(product_variant_id)
    
    def create_pos_variant(self, 
                          point_of_sale_id: int,
                          product_variant_id: int,
                          stock: int = 0,
                          price: Optional[float] = None) -> PointOfSaleProductVariant:
        """
        Create a new point of sale product variant.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            product_variant_id: The ID of the product variant.
            stock: The stock of the product variant at the point of sale.
            price: The price of the product variant at the point of sale.
            
        Returns:
            The created point of sale product variant.
        """
        pos_variant = PointOfSaleProductVariant(
            point_of_sale_id=point_of_sale_id,
            product_variant_id=product_variant_id,
            stock=stock,
            price=price
        )
        return self.pos_variant_repository.create(pos_variant)
    
    def update_pos_variant(self, 
                          pos_variant_id: int,
                          stock: Optional[int] = None,
                          price: Optional[float] = None) -> PointOfSaleProductVariant:
        """
        Update an existing point of sale product variant.
        
        Args:
            pos_variant_id: The ID of the point of sale product variant to update.
            stock: The new stock of the product variant at the point of sale.
            price: The new price of the product variant at the point of sale.
            
        Returns:
            The updated point of sale product variant.
            
        Raises:
            PointOfSaleProductVariantNotFoundError: If the point of sale product variant is not found.
        """
        pos_variant = self.get_pos_variant(pos_variant_id)
        
        if stock is not None:
            pos_variant.stock = stock
        
        if price is not None:
            pos_variant.price = price
        
        return self.pos_variant_repository.update(pos_variant)
    
    def delete_pos_variant(self, pos_variant_id: int) -> None:
        """
        Delete a point of sale product variant.
        
        Args:
            pos_variant_id: The ID of the point of sale product variant to delete.
            
        Raises:
            PointOfSaleProductVariantNotFoundError: If the point of sale product variant is not found.
        """
        # Check if the point of sale product variant exists
        self.get_pos_variant(pos_variant_id)
        
        self.pos_variant_repository.delete(pos_variant_id)

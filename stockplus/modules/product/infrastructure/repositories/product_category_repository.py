from typing import List, Optional

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from stockplus.modules.product.domain.exceptions import ProductCategoryNotFoundError
from stockplus.modules.product.domain.entities import ProductCategory as ProductCategoryDomain
from stockplus.modules.product.application.interfaces import IProductCategoryRepository
from stockplus.modules.product.infrastructure.models import ProductCategory as ProductCategoryORM

class ProductCategoryRepository(IProductCategoryRepository):
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
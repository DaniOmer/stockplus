from typing import List, Optional

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from stockplus.modules.product.domain.entities import Brand as BrandDomain
from stockplus.modules.product.application.interfaces import IBrandRepository
from stockplus.modules.product.infrastructure.models import Brand as BrandORM
from stockplus.modules.product.domain.exceptions import BrandNotFoundError

class BrandRepository(IBrandRepository):
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
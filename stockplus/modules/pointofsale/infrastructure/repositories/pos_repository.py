from typing import List, Optional

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from builder.models import User
from stockplus.modules.pointofsale.application.interfaces import PointOfSaleRepository
from stockplus.modules.pointofsale.domain.exceptions import (
    PointOfSaleNotFoundError, CollaboratorNotFoundError
)
from stockplus.modules.pointofsale.domain.entities import PointOfSale as PointOfSaleDomain
from stockplus.modules.pointofsale.infrastructure.models import PointOfSale


class PointOfSaleRepository(PointOfSaleRepository):
    """
    Django implementation of the point of sale repository.
    """
    
    def _to_domain(self, orm_point_of_sale: PointOfSale) -> PointOfSaleDomain:
        """
        Convert an ORM point of sale to a domain point of sale.
        
        Args:
            orm_point_of_sale: The ORM point of sale to convert.
            
        Returns:
            The domain point of sale.
        """
        collaborator_ids = list(orm_point_of_sale.collaborators.values_list('id', flat=True))
        
        return PointOfSaleDomain(
            id=orm_point_of_sale.id,
            uid=orm_point_of_sale.uid,
            name=orm_point_of_sale.name,
            type=orm_point_of_sale.type,
            company_id=orm_point_of_sale.company_id,
            opening_hours=orm_point_of_sale.opening_hours,
            closing_hours=orm_point_of_sale.closing_hours,
            collaborator_ids=collaborator_ids,
            is_active=not orm_point_of_sale.is_disable
        )
    
    def get_by_id(self, point_of_sale_id: int) -> Optional[PointOfSaleDomain]:
        """
        Get a point of sale by its ID.
        
        Args:
            point_of_sale_id: The ID of the point of sale to retrieve.
            
        Returns:
            The point of sale if found, None otherwise.
        """
        try:
            orm_point_of_sale = PointOfSale.objects.get(id=point_of_sale_id)
            return self._to_domain(orm_point_of_sale)
        except ObjectDoesNotExist:
            return None
    
    def get_by_company_id(self, company_id: int) -> List[PointOfSaleDomain]:
        """
        Get all points of sale for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of points of sale for the company.
        """
        orm_points_of_sale = PointOfSale.objects.filter(company_id=company_id)
        return [self._to_domain(pos) for pos in orm_points_of_sale]
    
    @transaction.atomic
    def create(self, point_of_sale: PointOfSaleDomain) -> PointOfSaleDomain:
        """
        Create a new point of sale.
        
        Args:
            point_of_sale: The point of sale to create.
            
        Returns:
            The created point of sale.
        """
        orm_point_of_sale = PointOfSale.objects.create(
            name=point_of_sale.name,
            company_id=point_of_sale.company_id,
            type=point_of_sale.type,
            opening_hours=point_of_sale.opening_hours,
            closing_hours=point_of_sale.closing_hours,
            is_disable=not point_of_sale.is_active
        )
        
        # Add collaborators if any
        if point_of_sale.collaborator_ids:
            collaborators = User.objects.filter(id__in=point_of_sale.collaborator_ids)
            orm_point_of_sale.collaborators.set(collaborators)
        
        return self._to_domain(orm_point_of_sale)
    
    @transaction.atomic
    def update(self, point_of_sale: PointOfSaleDomain) -> PointOfSaleDomain:
        """
        Update an existing point of sale.
        
        Args:
            point_of_sale: The point of sale to update.
            
        Returns:
            The updated point of sale.
            
        Raises:
            PointOfSaleNotFoundError: If the point of sale is not found.
        """
        try:
            orm_point_of_sale = PointOfSale.objects.get(id=point_of_sale.id)
        except ObjectDoesNotExist:
            raise PointOfSaleNotFoundError(point_of_sale.id)
        
        orm_point_of_sale.name = point_of_sale.name
        orm_point_of_sale.type = point_of_sale.type
        orm_point_of_sale.opening_hours = point_of_sale.opening_hours
        orm_point_of_sale.closing_hours = point_of_sale.closing_hours
        orm_point_of_sale.is_disable = not point_of_sale.is_active
        orm_point_of_sale.save()
        
        # Update collaborators if provided
        if point_of_sale.collaborator_ids:
            collaborators = User.objects.filter(id__in=point_of_sale.collaborator_ids)
            orm_point_of_sale.collaborators.set(collaborators)
        
        return self._to_domain(orm_point_of_sale)
    
    def delete(self, point_of_sale_id: int) -> None:
        """
        Delete a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale to delete.
            
        Raises:
            PointOfSaleNotFoundError: If the point of sale is not found.
        """
        try:
            orm_point_of_sale = PointOfSale.objects.get(id=point_of_sale_id)
            orm_point_of_sale.delete()
        except ObjectDoesNotExist:
            raise PointOfSaleNotFoundError(point_of_sale_id)
    
    @transaction.atomic
    def add_collaborator(self, point_of_sale_id: int, collaborator_id: int) -> PointOfSaleDomain:
        """
        Add a collaborator to a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            collaborator_id: The ID of the collaborator to add.
            
        Returns:
            The updated point of sale.
            
        Raises:
            PointOfSaleNotFoundError: If the point of sale is not found.
            CollaboratorNotFoundError: If the collaborator is not found.
        """
        try:
            orm_point_of_sale = PointOfSale.objects.get(id=point_of_sale_id)
        except ObjectDoesNotExist:
            raise PointOfSaleNotFoundError(point_of_sale_id)
        
        try:
            collaborator = User.objects.get(id=collaborator_id)
        except ObjectDoesNotExist:
            raise CollaboratorNotFoundError(message=f"Collaborator with id {collaborator_id} not found.")
        
        orm_point_of_sale.collaborators.add(collaborator)
        
        return self._to_domain(orm_point_of_sale)
    
    @transaction.atomic
    def remove_collaborator(self, point_of_sale_id: int, collaborator_id: int) -> PointOfSaleDomain:
        """
        Remove a collaborator from a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            collaborator_id: The ID of the collaborator to remove.
            
        Returns:
            The updated point of sale.
            
        Raises:
            PointOfSaleNotFoundError: If the point of sale is not found.
            CollaboratorNotFoundError: If the collaborator is not found.
        """
        try:
            orm_point_of_sale = PointOfSale.objects.get(id=point_of_sale_id)
        except ObjectDoesNotExist:
            raise PointOfSaleNotFoundError(point_of_sale_id)
        
        try:
            collaborator = User.objects.get(id=collaborator_id)
        except ObjectDoesNotExist:
            raise CollaboratorNotFoundError(message=f"Collaborator with id {collaborator_id} not found.")
        
        orm_point_of_sale.collaborators.remove(collaborator)
        
        return self._to_domain(orm_point_of_sale)

from typing import List, Optional

from stockplus.modules.pointofsale.application.interfaces import PointOfSaleRepository
from stockplus.modules.pointofsale.domain.exceptions import (
    PointOfSaleNotFoundError, CollaboratorNotFoundError, CompanyNotFoundError
)
from stockplus.modules.pointofsale.domain.models import PointOfSale


class PointOfSaleService:
    """
    Service for managing points of sale.
    """
    def __init__(self, point_of_sale_repository: PointOfSaleRepository):
        self.point_of_sale_repository = point_of_sale_repository
    
    def get_point_of_sale(self, point_of_sale_id: int) -> PointOfSale:
        """
        Get a point of sale by its ID.
        
        Args:
            point_of_sale_id: The ID of the point of sale to retrieve.
            
        Returns:
            The point of sale.
            
        Raises:
            PointOfSaleNotFoundError: If the point of sale is not found.
        """
        point_of_sale = self.point_of_sale_repository.get_by_id(point_of_sale_id)
        if not point_of_sale:
            raise PointOfSaleNotFoundError(point_of_sale_id)
        return point_of_sale
    
    def get_company_points_of_sale(self, company_id: int) -> List[PointOfSale]:
        """
        Get all points of sale for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of points of sale for the company.
        """
        return self.point_of_sale_repository.get_by_company_id(company_id)
    
    def create_point_of_sale(self, 
                            name: str, 
                            company_id: int, 
                            type: str = "store",
                            opening_hours: Optional[str] = None,
                            closing_hours: Optional[str] = None) -> PointOfSale:
        """
        Create a new point of sale.
        
        Args:
            name: The name of the point of sale.
            company_id: The ID of the company.
            type: The type of the point of sale.
            opening_hours: The opening hours of the point of sale.
            closing_hours: The closing hours of the point of sale.
            
        Returns:
            The created point of sale.
        """
        point_of_sale = PointOfSale(
            name=name,
            company_id=company_id,
            type=type,
            opening_hours=opening_hours,
            closing_hours=closing_hours
        )
        return self.point_of_sale_repository.create(point_of_sale)
    
    def update_point_of_sale(self, 
                            point_of_sale_id: int,
                            name: Optional[str] = None,
                            type: Optional[str] = None,
                            opening_hours: Optional[str] = None,
                            closing_hours: Optional[str] = None) -> PointOfSale:
        """
        Update an existing point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale to update.
            name: The new name of the point of sale.
            type: The new type of the point of sale.
            opening_hours: The new opening hours of the point of sale.
            closing_hours: The new closing hours of the point of sale.
            
        Returns:
            The updated point of sale.
            
        Raises:
            PointOfSaleNotFoundError: If the point of sale is not found.
        """
        point_of_sale = self.get_point_of_sale(point_of_sale_id)
        
        if name is not None:
            point_of_sale.name = name
        if type is not None:
            point_of_sale.type = type
        if opening_hours is not None:
            point_of_sale.opening_hours = opening_hours
        if closing_hours is not None:
            point_of_sale.closing_hours = closing_hours
        
        return self.point_of_sale_repository.update(point_of_sale)
    
    def delete_point_of_sale(self, point_of_sale_id: int) -> None:
        """
        Delete a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale to delete.
            
        Raises:
            PointOfSaleNotFoundError: If the point of sale is not found.
        """
        # Check if the point of sale exists
        self.get_point_of_sale(point_of_sale_id)
        
        self.point_of_sale_repository.delete(point_of_sale_id)
    
    def add_collaborator(self, point_of_sale_id: int, collaborator_id: int) -> PointOfSale:
        """
        Add a collaborator to a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            collaborator_id: The ID of the collaborator to add.
            
        Returns:
            The updated point of sale.
            
        Raises:
            PointOfSaleNotFoundError: If the point of sale is not found.
        """
        # Check if the point of sale exists
        self.get_point_of_sale(point_of_sale_id)
        
        return self.point_of_sale_repository.add_collaborator(point_of_sale_id, collaborator_id)
    
    def remove_collaborator(self, point_of_sale_id: int, collaborator_id: int) -> PointOfSale:
        """
        Remove a collaborator from a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            collaborator_id: The ID of the collaborator to remove.
            
        Returns:
            The updated point of sale.
            
        Raises:
            PointOfSaleNotFoundError: If the point of sale is not found.
        """
        # Check if the point of sale exists
        self.get_point_of_sale(point_of_sale_id)
        
        return self.point_of_sale_repository.remove_collaborator(point_of_sale_id, collaborator_id)

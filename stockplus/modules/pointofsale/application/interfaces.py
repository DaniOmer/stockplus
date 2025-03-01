from abc import ABC, abstractmethod
from typing import List, Optional

from stockplus.modules.pointofsale.domain.models import PointOfSale


class PointOfSaleRepository(ABC):
    """
    Interface for the point of sale repository.
    """
    @abstractmethod
    def get_by_id(self, point_of_sale_id: int) -> Optional[PointOfSale]:
        """
        Get a point of sale by its ID.
        
        Args:
            point_of_sale_id: The ID of the point of sale to retrieve.
            
        Returns:
            The point of sale if found, None otherwise.
        """
        pass
    
    @abstractmethod
    def get_by_company_id(self, company_id: int) -> List[PointOfSale]:
        """
        Get all points of sale for a company.
        
        Args:
            company_id: The ID of the company.
            
        Returns:
            A list of points of sale for the company.
        """
        pass
    
    @abstractmethod
    def create(self, point_of_sale: PointOfSale) -> PointOfSale:
        """
        Create a new point of sale.
        
        Args:
            point_of_sale: The point of sale to create.
            
        Returns:
            The created point of sale.
        """
        pass
    
    @abstractmethod
    def update(self, point_of_sale: PointOfSale) -> PointOfSale:
        """
        Update an existing point of sale.
        
        Args:
            point_of_sale: The point of sale to update.
            
        Returns:
            The updated point of sale.
        """
        pass
    
    @abstractmethod
    def delete(self, point_of_sale_id: int) -> None:
        """
        Delete a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale to delete.
        """
        pass
    
    @abstractmethod
    def add_collaborator(self, point_of_sale_id: int, collaborator_id: int) -> PointOfSale:
        """
        Add a collaborator to a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            collaborator_id: The ID of the collaborator to add.
            
        Returns:
            The updated point of sale.
        """
        pass
    
    @abstractmethod
    def remove_collaborator(self, point_of_sale_id: int, collaborator_id: int) -> PointOfSale:
        """
        Remove a collaborator from a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            collaborator_id: The ID of the collaborator to remove.
            
        Returns:
            The updated point of sale.
        """
        pass

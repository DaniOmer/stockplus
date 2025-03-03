from abc import ABC, abstractmethod
from typing import List, Optional

from stockplus.modules.pointofsale.domain.entities import PointOfSale, PosPaymentMethod


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


class PaymentMethodRepository(ABC):
    """
    Interface for the payment method repository.
    """
    @abstractmethod
    def get_by_id(self, payment_method_id: int) -> Optional[PosPaymentMethod]:
        """
        Get a payment method by its ID.
        
        Args:
            payment_method_id: The ID of the payment method to retrieve.
            
        Returns:
            The payment method if found, None otherwise.
        """
        pass
    
    @abstractmethod
    def get_by_point_of_sale_id(self, point_of_sale_id: int) -> List[PosPaymentMethod]:
        """
        Get all payment methods for a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            
        Returns:
            A list of payment methods for the point of sale.
        """
        pass
    
    @abstractmethod
    def create(self, payment_method: PosPaymentMethod) -> PosPaymentMethod:
        """
        Create a new payment method.
        
        Args:
            payment_method: The payment method to create.
            
        Returns:
            The created payment method.
        """
        pass
    
    @abstractmethod
    def update(self, payment_method: PosPaymentMethod) -> PosPaymentMethod:
        """
        Update an existing payment method.
        
        Args:
            payment_method: The payment method to update.
            
        Returns:
            The updated payment method.
        """
        pass
    
    @abstractmethod
    def delete(self, payment_method_id: int) -> None:
        """
        Delete a payment method.
        
        Args:
            payment_method_id: The ID of the payment method to delete.
        """
        pass
    
    @abstractmethod
    def toggle_status(self, payment_method_id: int) -> PosPaymentMethod:
        """
        Toggle the active status of a payment method.
        
        Args:
            payment_method_id: The ID of the payment method.
            
        Returns:
            The updated payment method.
        """
        pass

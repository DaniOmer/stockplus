from typing import List, Optional

from stockplus.modules.pointofsale.application.interfaces import PointOfSaleRepository, PaymentMethodRepository
from stockplus.modules.pointofsale.domain.exceptions import (
    PointOfSaleNotFoundError,
    PaymentMethodNotFoundError,
    PointOfSaleLimitExceededError
)
from stockplus.modules.pointofsale.domain.entities import PointOfSale, PosPaymentMethod
from stockplus.modules.subscription.services.subscription_service import SubscriptionService


class PointOfSaleService:
    """
    Service for managing points of sale.
    """
    def __init__(self, point_of_sale_repository: PointOfSaleRepository):
        self.point_of_sale_repository = point_of_sale_repository
        self.subscription_service = None
    
    def get_subscription_service(self):
        """
        Get the subscription service.
        
        Returns:
            The subscription service.
        """
        if not self.subscription_service:
            from stockplus.config.dependencies import get_subscription_service
            self.subscription_service = get_subscription_service()
        return self.subscription_service
    
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
    
    def validate_pos_limit(self, company_id: int) -> None:
        """
        Validate that the company has not exceeded its point of sale limit.
        
        Args:
            company_id: The ID of the company.
            
        Raises:
            PointOfSaleLimitExceededError: If the company has exceeded its point of sale limit.
        """
        # Get the company's subscription
        subscription_service = self.get_subscription_service()
        subscription = subscription_service.get_company_subscription(company_id)
        
        if not subscription or not subscription.subscription_plan:
            # If no subscription or no plan, assume free trial with default limit
            pos_limit = 3
        else:
            # Get the POS limit from the subscription plan
            pos_limit = subscription.subscription_plan.pos_limit
        
        # Count the company's active points of sale
        pos_count = len(self.get_company_points_of_sale(company_id))
        
        # Check if the company has exceeded its limit (0 means unlimited)
        if pos_limit > 0 and pos_count >= pos_limit:
            raise PointOfSaleLimitExceededError(
                company_id=company_id,
                current_count=pos_count,
                limit=pos_limit
            )
    
    def create_point_of_sale(self, 
                            name: str, 
                            company_id: int, 
                            type: str = "store",
                            opening_hours: Optional[str] = None,
                            closing_hours: Optional[str] = None,
                            is_default: bool = False) -> PointOfSale:
        """
        Create a new point of sale.
        
        Args:
            name: The name of the point of sale.
            company_id: The ID of the company.
            type: The type of the point of sale.
            opening_hours: The opening hours of the point of sale.
            closing_hours: The closing hours of the point of sale.
            is_default: Whether this is the default point of sale.
            
        Returns:
            The created point of sale.
            
        Raises:
            PointOfSaleLimitExceededError: If the company has exceeded its point of sale limit.
        """
        # Validate that the company has not exceeded its point of sale limit
        self.validate_pos_limit(company_id)
        
        point_of_sale = PointOfSale(
            name=name,
            company_id=company_id,
            type=type,
            opening_hours=opening_hours,
            closing_hours=closing_hours,
            is_default=is_default
        )
        return self.point_of_sale_repository.create(point_of_sale)
    
    def update_point_of_sale(self, 
                            point_of_sale_id: int,
                            name: Optional[str] = None,
                            type: Optional[str] = None,
                            opening_hours: Optional[str] = None,
                            closing_hours: Optional[str] = None,
                            is_default: Optional[bool] = None) -> PointOfSale:
        """
        Update an existing point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale to update.
            name: The new name of the point of sale.
            type: The new type of the point of sale.
            opening_hours: The new opening hours of the point of sale.
            closing_hours: The new closing hours of the point of sale.
            is_default: Whether this is the default point of sale.
            
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
        if is_default is not None:
            point_of_sale.is_default = is_default
        
        return self.point_of_sale_repository.update(point_of_sale)
    
    def set_default_point_of_sale(self, point_of_sale_id: int) -> PointOfSale:
        """
        Set a point of sale as the default for a company.
        
        Args:
            point_of_sale_id: The ID of the point of sale to set as default.
            
        Returns:
            The updated point of sale.
            
        Raises:
            PointOfSaleNotFoundError: If the point of sale is not found.
        """
        point_of_sale = self.get_point_of_sale(point_of_sale_id)
        point_of_sale.is_default = True
        
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


class PaymentMethodService:
    """
    Service for managing payment methods.
    """
    def __init__(self, payment_method_repository: PaymentMethodRepository, point_of_sale_service: PointOfSaleService):
        self.payment_method_repository = payment_method_repository
        self.point_of_sale_service = point_of_sale_service
    
    def get_payment_method(self, payment_method_id: int) -> PosPaymentMethod:
        """
        Get a payment method by its ID.
        
        Args:
            payment_method_id: The ID of the payment method to retrieve.
            
        Returns:
            The payment method.
            
        Raises:
            PaymentMethodNotFoundError: If the payment method is not found.
        """
        payment_method = self.payment_method_repository.get_by_id(payment_method_id)
        if not payment_method:
            raise PaymentMethodNotFoundError(payment_method_id)
        return payment_method
    
    def get_point_of_sale_payment_methods(self, point_of_sale_id: int) -> List[PosPaymentMethod]:
        """
        Get all payment methods for a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            
        Returns:
            A list of payment methods for the point of sale.
            
        Raises:
            PointOfSaleNotFoundError: If the point of sale is not found.
        """
        # Check if the point of sale exists
        self.point_of_sale_service.get_point_of_sale(point_of_sale_id)
        
        return self.payment_method_repository.get_by_point_of_sale_id(point_of_sale_id)
    
    def create_payment_method(self, 
                             name: str, 
                             point_of_sale_id: int, 
                             description: Optional[str] = None,
                             requires_confirmation: bool = False,
                             confirmation_instructions: Optional[str] = None) -> PosPaymentMethod:
        """
        Create a new payment method.
        
        Args:
            name: The name of the payment method.
            point_of_sale_id: The ID of the point of sale.
            description: The description of the payment method.
            requires_confirmation: Whether the payment method requires confirmation.
            confirmation_instructions: Instructions for confirming the payment.
            
        Returns:
            The created payment method.
            
        Raises:
            PointOfSaleNotFoundError: If the point of sale is not found.
        """
        # Check if the point of sale exists
        self.point_of_sale_service.get_point_of_sale(point_of_sale_id)
        
        payment_method = PosPaymentMethod(
            name=name,
            point_of_sale_id=point_of_sale_id,
            description=description,
            requires_confirmation=requires_confirmation,
            confirmation_instructions=confirmation_instructions
        )
        return self.payment_method_repository.create(payment_method)
    
    def update_payment_method(self, 
                             payment_method_id: int,
                             name: Optional[str] = None,
                             description: Optional[str] = None,
                             requires_confirmation: Optional[bool] = None,
                             confirmation_instructions: Optional[str] = None) -> PosPaymentMethod:
        """
        Update an existing payment method.
        
        Args:
            payment_method_id: The ID of the payment method to update.
            name: The new name of the payment method.
            description: The new description of the payment method.
            requires_confirmation: Whether the payment method requires confirmation.
            confirmation_instructions: Instructions for confirming the payment.
            
        Returns:
            The updated payment method.
            
        Raises:
            PaymentMethodNotFoundError: If the payment method is not found.
        """
        payment_method = self.get_payment_method(payment_method_id)
        
        if name is not None:
            payment_method.name = name
        if description is not None:
            payment_method.description = description
        if requires_confirmation is not None:
            payment_method.requires_confirmation = requires_confirmation
        if confirmation_instructions is not None:
            payment_method.confirmation_instructions = confirmation_instructions
        
        return self.payment_method_repository.update(payment_method)
    
    def delete_payment_method(self, payment_method_id: int) -> None:
        """
        Delete a payment method.
        
        Args:
            payment_method_id: The ID of the payment method to delete.
            
        Raises:
            PaymentMethodNotFoundError: If the payment method is not found.
        """
        # Check if the payment method exists
        self.get_payment_method(payment_method_id)
        
        self.payment_method_repository.delete(payment_method_id)
    
    def toggle_payment_method_status(self, payment_method_id: int) -> PosPaymentMethod:
        """
        Toggle the active status of a payment method.
        
        Args:
            payment_method_id: The ID of the payment method.
            
        Returns:
            The updated payment method.
            
        Raises:
            PaymentMethodNotFoundError: If the payment method is not found.
        """
        # Check if the payment method exists
        self.get_payment_method(payment_method_id)
        
        return self.payment_method_repository.toggle_status(payment_method_id)

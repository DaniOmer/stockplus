from typing import List, Optional

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from stockplus.modules.pointofsale.application.interfaces import PaymentMethodRepository
from stockplus.modules.pointofsale.domain.exceptions import PaymentMethodNotFoundError
from stockplus.modules.pointofsale.domain.entities import PaymentMethod as PaymentMethodDomain
from stockplus.modules.pointofsale.infrastructure.models import PosPaymentMethod


class PointOfSalePaymentMethodRepository(PaymentMethodRepository):
    """
    Django implementation of the payment method repository.
    """
    
    def _to_domain(self, orm_payment_method: PosPaymentMethod) -> PaymentMethodDomain:
        """
        Convert an ORM payment method to a domain payment method.
        
        Args:
            orm_payment_method: The ORM payment method to convert.
            
        Returns:
            The domain payment method.
        """
        return PaymentMethodDomain(
            id=orm_payment_method.id,
            uid=orm_payment_method.uid,
            name=orm_payment_method.name,
            description=orm_payment_method.description,
            point_of_sale_id=orm_payment_method.point_of_sale_id,
            is_active= not orm_payment_method.is_disable,
            requires_confirmation=orm_payment_method.requires_confirmation,
            confirmation_instructions=orm_payment_method.confirmation_instructions
        )
    
    def get_by_id(self, payment_method_id: int) -> Optional[PaymentMethodDomain]:
        """
        Get a payment method by its ID.
        
        Args:
            payment_method_id: The ID of the payment method to retrieve.
            
        Returns:
            The payment method if found, None otherwise.
        """
        try:
            orm_payment_method = PosPaymentMethod.objects.get(id=payment_method_id)
            return self._to_domain(orm_payment_method)
        except ObjectDoesNotExist:
            return None
    
    def get_by_point_of_sale_id(self, point_of_sale_id: int) -> List[PaymentMethodDomain]:
        """
        Get all payment methods for a point of sale.
        
        Args:
            point_of_sale_id: The ID of the point of sale.
            
        Returns:
            A list of payment methods for the point of sale.
        """
        orm_payment_methods = PosPaymentMethod.objects.filter(point_of_sale_id=point_of_sale_id)
        return [self._to_domain(pm) for pm in orm_payment_methods]
    
    @transaction.atomic
    def create(self, payment_method: PaymentMethodDomain) -> PaymentMethodDomain:
        """
        Create a new payment method.
        
        Args:
            payment_method: The payment method to create.
            
        Returns:
            The created payment method.
        """
        orm_payment_method = PosPaymentMethod.objects.create(
            name=payment_method.name,
            description=payment_method.description,
            point_of_sale_id=payment_method.point_of_sale_id,
            is_disable= not payment_method.is_active,
            requires_confirmation=payment_method.requires_confirmation,
            confirmation_instructions=payment_method.confirmation_instructions
        )
        
        return self._to_domain(orm_payment_method)
    
    @transaction.atomic
    def update(self, payment_method: PaymentMethodDomain) -> PaymentMethodDomain:
        """
        Update an existing payment method.
        
        Args:
            payment_method: The payment method to update.
            
        Returns:
            The updated payment method.
            
        Raises:
            PaymentMethodNotFoundError: If the payment method is not found.
        """
        try:
            orm_payment_method = PosPaymentMethod.objects.get(id=payment_method.id)
        except ObjectDoesNotExist:
            raise PaymentMethodNotFoundError(payment_method.id)
        
        orm_payment_method.name = payment_method.name
        orm_payment_method.description = payment_method.description
        orm_payment_method.is_disable = not payment_method.is_active
        orm_payment_method.requires_confirmation = payment_method.requires_confirmation
        orm_payment_method.confirmation_instructions = payment_method.confirmation_instructions
        orm_payment_method.save()
        
        return self._to_domain(orm_payment_method)
    
    def delete(self, payment_method_id: int) -> None:
        """
        Delete a payment method.
        
        Args:
            payment_method_id: The ID of the payment method to delete.
            
        Raises:
            PaymentMethodNotFoundError: If the payment method is not found.
        """
        try:
            orm_payment_method = PosPaymentMethod.objects.get(id=payment_method_id)
            orm_payment_method.delete()
        except ObjectDoesNotExist:
            raise PaymentMethodNotFoundError(payment_method_id)
    
    @transaction.atomic
    def toggle_status(self, payment_method_id: int) -> PaymentMethodDomain:
        """
        Toggle the active status of a payment method.
        
        Args:
            payment_method_id: The ID of the payment method.
            
        Returns:
            The updated payment method.
            
        Raises:
            PaymentMethodNotFoundError: If the payment method is not found.
        """
        try:
            orm_payment_method = PosPaymentMethod.objects.get(id=payment_method_id)
        except ObjectDoesNotExist:
            raise PaymentMethodNotFoundError(payment_method_id)
        
        orm_payment_method.is_disable = not orm_payment_method.is_disable
        orm_payment_method.save()
        
        return self._to_domain(orm_payment_method)

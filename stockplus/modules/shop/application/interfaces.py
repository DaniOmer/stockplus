from abc import ABC, abstractmethod
from typing import List, Optional

from stockplus.modules.shop.domain.entities import Customer, Product, Price


class ICustomerRepository(ABC):
    """
    Interface for the customer repository.
    """
    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """
        Get a customer by its ID.
        
        Args:
            customer_id: The ID of the customer to retrieve.
            
        Returns:
            The customer, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[Customer]:
        """
        Get a customer by its user ID.
        
        Args:
            user_id: The ID of the user.
            
        Returns:
            The customer, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_stripe_id(self, stripe_id: str) -> Optional[Customer]:
        """
        Get a customer by its Stripe ID.
        
        Args:
            stripe_id: The Stripe ID of the customer.
            
        Returns:
            The customer, or None if not found.
        """
        pass
    
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """
        Create a new customer.
        
        Args:
            customer: The customer to create.
            
        Returns:
            The created customer.
        """
        pass
    
    @abstractmethod
    def update(self, customer: Customer) -> Customer:
        """
        Update an existing customer.
        
        Args:
            customer: The customer to update.
            
        Returns:
            The updated customer.
        """
        pass
    
    @abstractmethod
    def delete(self, customer_id: int) -> None:
        """
        Delete a customer.
        
        Args:
            customer_id: The ID of the customer to delete.
        """
        pass


class IProductRepository(ABC):
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
            The product, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Product]:
        """
        Get a product by its name.
        
        Args:
            name: The name of the product to retrieve.
            
        Returns:
            The product, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_stripe_id(self, stripe_id: str) -> Optional[Product]:
        """
        Get a product by its Stripe ID.
        
        Args:
            stripe_id: The Stripe ID of the product.
            
        Returns:
            The product, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_all_active(self) -> List[Product]:
        """
        Get all active products.
        
        Returns:
            A list of active products.
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


class IPriceRepository(ABC):
    """
    Interface for the price repository.
    """
    @abstractmethod
    def get_by_id(self, price_id: int) -> Optional[Price]:
        """
        Get a price by its ID.
        
        Args:
            price_id: The ID of the price to retrieve.
            
        Returns:
            The price, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_by_product_id(self, product_id: int) -> List[Price]:
        """
        Get all prices for a product.
        
        Args:
            product_id: The ID of the product.
            
        Returns:
            A list of prices for the product.
        """
        pass
    
    @abstractmethod
    def get_by_stripe_id(self, stripe_id: str) -> Optional[Price]:
        """
        Get a price by its Stripe ID.
        
        Args:
            stripe_id: The Stripe ID of the price.
            
        Returns:
            The price, or None if not found.
        """
        pass
    
    @abstractmethod
    def create(self, price: Price) -> Price:
        """
        Create a new price.
        
        Args:
            price: The price to create.
            
        Returns:
            The created price.
        """
        pass
    
    @abstractmethod
    def update(self, price: Price) -> Price:
        """
        Update an existing price.
        
        Args:
            price: The price to update.
            
        Returns:
            The updated price.
        """
        pass
    
    @abstractmethod
    def delete(self, price_id: int) -> None:
        """
        Delete a price.
        
        Args:
            price_id: The ID of the price to delete.
        """
        pass

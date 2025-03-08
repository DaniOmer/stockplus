"""
Shop services for the shop application.
This module contains the services for the shop application.
"""

import logging
import stripe
import sentry_sdk
from typing import List, Optional
from django.conf import settings

from stockplus.modules.shop.application.interfaces import (
    ICustomerRepository,
    IProductRepository,
    IPriceRepository
)
from stockplus.modules.shop.domain.entities import (
    Customer,
    Product,
    Price
)
from stockplus.modules.shop.domain.exceptions import (
    CustomerNotFoundError,
    ProductNotFoundError,
    PriceNotFoundError,
    CustomerAlreadyExistsError,
    ProductAlreadyExistsError,
    StripeError
)

logger = logging.getLogger(__name__)

# Configure Stripe API key
if hasattr(settings, 'STRIPE_SECRET_KEY'):
    stripe.api_key = settings.STRIPE_SECRET_KEY
else:
    logger.error("STRIPE_SECRET_KEY is not set in settings. Stripe integration will not work.")


class CustomerService:
    """
    Service for managing customers.
    """
    def __init__(self, customer_repository: ICustomerRepository):
        self.customer_repository = customer_repository
    
    def get_customer(self, customer_id: int) -> Customer:
        """
        Get a customer by ID.
        
        Args:
            customer_id: The ID of the customer
            
        Returns:
            Customer: The customer
            
        Raises:
            CustomerNotFoundError: If the customer is not found
        """
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError(customer_id)
        return customer
    
    def get_customer_by_user_id(self, user_id: int) -> Optional[Customer]:
        """
        Get a customer by user ID.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            Optional[Customer]: The customer, or None if not found
        """
        return self.customer_repository.get_by_user_id(user_id)
    
    def create_customer(self, user_id: int) -> Customer:
        """
        Create a customer for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            Customer: The created customer
            
        Raises:
            CustomerAlreadyExistsError: If the user already has a customer
        """
        # Check if the user already has a customer
        existing_customer = self.get_customer_by_user_id(user_id)
        if existing_customer:
            raise CustomerAlreadyExistsError(user_id)
        
        # Create a Stripe customer
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=user_id)
            
            stripe_customer = stripe.Customer.create(
                email=user.email,
                name=f"{user.first_name} {user.last_name}",
                metadata={
                    'user_id': user_id
                }
            )
            
            # Create the customer
            customer = Customer(
                user_id=user_id,
                stripe_id=stripe_customer.id
            )
            
            return self.customer_repository.create(customer)
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            sentry_sdk.capture_exception(e)
            raise StripeError(str(e))
    
    def update_customer(self, customer: Customer) -> Customer:
        """
        Update a customer.
        
        Args:
            customer: The customer to update
            
        Returns:
            Customer: The updated customer
            
        Raises:
            CustomerNotFoundError: If the customer is not found
        """
        # Check if the customer exists
        existing_customer = self.customer_repository.get_by_id(customer.id)
        if not existing_customer:
            raise CustomerNotFoundError(customer.id)
        
        # Update the customer in Stripe
        try:
            if customer.stripe_id:
                stripe.Customer.modify(
                    customer.stripe_id,
                    metadata={
                        'user_id': customer.user_id
                    }
                )
        except Exception as e:
            logger.error(f"Error updating Stripe customer: {e}")
            sentry_sdk.capture_exception(e)
            raise StripeError(str(e))
        
        # Update the customer
        return self.customer_repository.update(customer)
    
    def delete_customer(self, customer_id: int) -> None:
        """
        Delete a customer.
        
        Args:
            customer_id: The ID of the customer to delete
            
        Raises:
            CustomerNotFoundError: If the customer is not found
        """
        # Check if the customer exists
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError(customer_id)
        
        # Delete the customer in Stripe
        try:
            if customer.stripe_id:
                stripe.Customer.delete(customer.stripe_id)
        except Exception as e:
            logger.error(f"Error deleting Stripe customer: {e}")
            sentry_sdk.capture_exception(e)
            raise StripeError(str(e))
        
        # Delete the customer
        self.customer_repository.delete(customer_id)


class ProductService:
    """
    Service for managing products.
    """
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository
    
    def get_product(self, product_id: int) -> Product:
        """
        Get a product by ID.
        
        Args:
            product_id: The ID of the product
            
        Returns:
            Product: The product
            
        Raises:
            ProductNotFoundError: If the product is not found
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return product
    
    def get_product_by_name(self, name: str) -> Optional[Product]:
        """
        Get a product by name.
        
        Args:
            name: The name of the product
            
        Returns:
            Optional[Product]: The product, or None if not found
        """
        return self.product_repository.get_by_name(name)
    
    def get_all_active_products(self) -> List[Product]:
        """
        Get all active products.
        
        Returns:
            List[Product]: A list of active products
        """
        return self.product_repository.get_all_active()
    
    def create_product(self, name: str, description: str = None, active: bool = True) -> Product:
        """
        Create a product.
        
        Args:
            name: The name of the product
            description: The description of the product
            active: Whether the product is active
            
        Returns:
            Product: The created product
            
        Raises:
            ProductAlreadyExistsError: If a product with the same name already exists
        """
        # Check if a product with the same name already exists
        existing_product = self.get_product_by_name(name)
        if existing_product:
            raise ProductAlreadyExistsError(name)
        
        # Create a Stripe product
        try:
            stripe_product = stripe.Product.create(
                name=name,
                description=description if description else name,
                active=active,
                metadata={
                    'product_name': name
                }
            )
            
            # Create the product
            product = Product(
                name=name,
                description=description,
                active=active,
                stripe_id=stripe_product.id
            )
            
            return self.product_repository.create(product)
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            sentry_sdk.capture_exception(e)
            raise StripeError(str(e))
    
    def update_product(self, product: Product) -> Product:
        """
        Update a product.
        
        Args:
            product: The product to update
            
        Returns:
            Product: The updated product
            
        Raises:
            ProductNotFoundError: If the product is not found
        """
        # Check if the product exists
        existing_product = self.product_repository.get_by_id(product.id)
        if not existing_product:
            raise ProductNotFoundError(product.id)
        
        # Update the product in Stripe
        try:
            if product.stripe_id:
                stripe.Product.modify(
                    product.stripe_id,
                    name=product.name,
                    description=product.description if product.description else product.name,
                    active=product.active,
                    metadata={
                        'product_name': product.name
                    }
                )
        except Exception as e:
            logger.error(f"Error updating Stripe product: {e}")
            sentry_sdk.capture_exception(e)
            raise StripeError(str(e))
        
        # Update the product
        return self.product_repository.update(product)
    
    def delete_product(self, product_id: int) -> None:
        """
        Delete a product.
        
        Args:
            product_id: The ID of the product to delete
            
        Raises:
            ProductNotFoundError: If the product is not found
        """
        # Check if the product exists
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        
        # Delete the product in Stripe
        try:
            if product.stripe_id:
                # In Stripe, products are archived, not deleted
                stripe.Product.modify(
                    product.stripe_id,
                    active=False
                )
        except Exception as e:
            logger.error(f"Error deleting Stripe product: {e}")
            sentry_sdk.capture_exception(e)
            raise StripeError(str(e))
        
        # Delete the product
        self.product_repository.delete(product_id)


class PriceService:
    """
    Service for managing prices.
    """
    def __init__(self, price_repository: IPriceRepository, product_repository: IProductRepository):
        self.price_repository = price_repository
        self.product_repository = product_repository
    
    def get_price(self, price_id: int) -> Price:
        """
        Get a price by ID.
        
        Args:
            price_id: The ID of the price
            
        Returns:
            Price: The price
            
        Raises:
            PriceNotFoundError: If the price is not found
        """
        price = self.price_repository.get_by_id(price_id)
        if not price:
            raise PriceNotFoundError(price_id)
        return price
    
    def get_prices_by_product_id(self, product_id: int) -> List[Price]:
        """
        Get all prices for a product.
        
        Args:
            product_id: The ID of the product
            
        Returns:
            List[Price]: A list of prices for the product
        """
        return self.price_repository.get_by_product_id(product_id)
    
    def create_price(self, product_id: int, unit_amount: int, currency: str = 'eur',
                    interval: str = None, interval_count: int = None) -> Price:
        """
        Create a price.
        
        Args:
            product_id: The ID of the product
            unit_amount: The amount in cents
            currency: The currency
            interval: The interval (day, week, month, year)
            interval_count: The interval count
            
        Returns:
            Price: The created price
            
        Raises:
            ProductNotFoundError: If the product is not found
        """
        # Check if the product exists
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        
        # Create a Stripe price
        try:
            stripe_price_data = {
                'unit_amount': unit_amount,
                'currency': currency,
                'product': product.stripe_id,
                'metadata': {
                    'product_id': product_id
                }
            }
            
            # Add recurring parameters if interval is provided
            if interval:
                stripe_price_data['recurring'] = {
                    'interval': interval,
                    'interval_count': interval_count or 1
                }
            
            stripe_price = stripe.Price.create(**stripe_price_data)
            
            # Create the price
            price = Price(
                product_id=product_id,
                unit_amount=unit_amount,
                currency=currency,
                interval=interval,
                interval_count=interval_count,
                stripe_id=stripe_price.id
            )
            
            return self.price_repository.create(price)
        except Exception as e:
            logger.error(f"Error creating price: {e}")
            sentry_sdk.capture_exception(e)
            raise StripeError(str(e))
    
    def update_price(self, price: Price) -> Price:
        """
        Update a price.
        
        Args:
            price: The price to update
            
        Returns:
            Price: The updated price
            
        Raises:
            PriceNotFoundError: If the price is not found
            ProductNotFoundError: If the product is not found
        """
        # Check if the price exists
        existing_price = self.price_repository.get_by_id(price.id)
        if not existing_price:
            raise PriceNotFoundError(price.id)
        
        # Check if the product exists
        product = self.product_repository.get_by_id(price.product_id)
        if not product:
            raise ProductNotFoundError(price.product_id)
        
        # In Stripe, prices cannot be updated, only created
        # So we'll create a new price and archive the old one
        try:
            if price.stripe_id:
                # Archive the old price
                stripe.Price.modify(
                    price.stripe_id,
                    active=False
                )
            
            # Create a new price
            stripe_price_data = {
                'unit_amount': price.unit_amount,
                'currency': price.currency,
                'product': product.stripe_id,
                'metadata': {
                    'product_id': price.product_id
                }
            }
            
            # Add recurring parameters if interval is provided
            if price.interval:
                stripe_price_data['recurring'] = {
                    'interval': price.interval,
                    'interval_count': price.interval_count or 1
                }
            
            stripe_price = stripe.Price.create(**stripe_price_data)
            
            # Update the price with the new Stripe ID
            price.stripe_id = stripe_price.id
        except Exception as e:
            logger.error(f"Error updating Stripe price: {e}")
            sentry_sdk.capture_exception(e)
            raise StripeError(str(e))
        
        # Update the price
        return self.price_repository.update(price)
    
    def delete_price(self, price_id: int) -> None:
        """
        Delete a price.
        
        Args:
            price_id: The ID of the price to delete
            
        Raises:
            PriceNotFoundError: If the price is not found
        """
        # Check if the price exists
        price = self.price_repository.get_by_id(price_id)
        if not price:
            raise PriceNotFoundError(price_id)
        
        # Delete the price in Stripe
        try:
            if price.stripe_id:
                # In Stripe, prices are archived, not deleted
                stripe.Price.modify(
                    price.stripe_id,
                    active=False
                )
        except Exception as e:
            logger.error(f"Error deleting Stripe price: {e}")
            sentry_sdk.capture_exception(e)
            raise StripeError(str(e))
        
        # Delete the price
        self.price_repository.delete(price_id)

from typing import List, Optional
from uuid import uuid4

from django.db import transaction

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
    PriceNotFoundError
)
from stockplus.modules.shop.infrastructure.models import (
    Customer as CustomerORM,
    Product as ProductORM,
    Price as PriceORM
)


class CustomerRepository(ICustomerRepository):
    """
    Implementation of the customer repository.
    """
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """
        Get a customer by its ID.
        
        Args:
            customer_id: The ID of the customer to retrieve.
            
        Returns:
            The customer, or None if not found.
        """
        try:
            customer_orm = CustomerORM.objects.get(id=customer_id)
            return self._to_domain(customer_orm)
        except CustomerORM.DoesNotExist:
            return None
    
    def get_by_user_id(self, user_id: int) -> Optional[Customer]:
        """
        Get a customer by its user ID.
        
        Args:
            user_id: The ID of the user.
            
        Returns:
            The customer, or None if not found.
        """
        try:
            customer_orm = CustomerORM.objects.get(user_id=user_id)
            return self._to_domain(customer_orm)
        except CustomerORM.DoesNotExist:
            return None
    
    def get_by_stripe_id(self, stripe_id: str) -> Optional[Customer]:
        """
        Get a customer by its Stripe ID.
        
        Args:
            stripe_id: The Stripe ID of the customer.
            
        Returns:
            The customer, or None if not found.
        """
        try:
            customer_orm = CustomerORM.objects.get(stripe_id=stripe_id)
            return self._to_domain(customer_orm)
        except CustomerORM.DoesNotExist:
            return None
    
    def create(self, customer: Customer) -> Customer:
        """
        Create a new customer.
        
        Args:
            customer: The customer to create.
            
        Returns:
            The created customer.
        """
        customer_orm = CustomerORM(
            uid=uuid4() if not customer.uid else customer.uid,
            user_id=customer.user_id,
            stripe_id=customer.stripe_id
        )
        customer_orm.save()
        
        return self._to_domain(customer_orm)
    
    def update(self, customer: Customer) -> Customer:
        """
        Update an existing customer.
        
        Args:
            customer: The customer to update.
            
        Returns:
            The updated customer.
        """
        try:
            customer_orm = CustomerORM.objects.get(id=customer.id)
        except CustomerORM.DoesNotExist:
            raise CustomerNotFoundError(customer.id)
        
        customer_orm.user_id = customer.user_id
        customer_orm.stripe_id = customer.stripe_id
        customer_orm.save()
        
        return self._to_domain(customer_orm)
    
    def delete(self, customer_id: int) -> None:
        """
        Delete a customer.
        
        Args:
            customer_id: The ID of the customer to delete.
        """
        try:
            customer_orm = CustomerORM.objects.get(id=customer_id)
            customer_orm.delete()
        except CustomerORM.DoesNotExist:
            raise CustomerNotFoundError(customer_id)
    
    def _to_domain(self, customer_orm: CustomerORM) -> Customer:
        """
        Convert an ORM customer to a domain customer.
        
        Args:
            customer_orm: The ORM customer to convert.
            
        Returns:
            The domain customer.
        """
        return Customer(
            id=customer_orm.id,
            uid=customer_orm.uid,
            user_id=customer_orm.user_id,
            stripe_id=customer_orm.stripe_id,
            is_active=customer_orm.is_active
        )


class ProductRepository(IProductRepository):
    """
    Implementation of the product repository.
    """
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Get a product by its ID.
        
        Args:
            product_id: The ID of the product to retrieve.
            
        Returns:
            The product, or None if not found.
        """
        try:
            product_orm = ProductORM.objects.get(id=product_id)
            return self._to_domain(product_orm)
        except ProductORM.DoesNotExist:
            return None
    
    def get_by_name(self, name: str) -> Optional[Product]:
        """
        Get a product by its name.
        
        Args:
            name: The name of the product to retrieve.
            
        Returns:
            The product, or None if not found.
        """
        try:
            product_orm = ProductORM.objects.get(name=name)
            return self._to_domain(product_orm)
        except ProductORM.DoesNotExist:
            return None
    
    def get_by_stripe_id(self, stripe_id: str) -> Optional[Product]:
        """
        Get a product by its Stripe ID.
        
        Args:
            stripe_id: The Stripe ID of the product.
            
        Returns:
            The product, or None if not found.
        """
        try:
            product_orm = ProductORM.objects.get(stripe_id=stripe_id)
            return self._to_domain(product_orm)
        except ProductORM.DoesNotExist:
            return None
    
    def get_all_active(self) -> List[Product]:
        """
        Get all active products.
        
        Returns:
            A list of active products.
        """
        products_orm = ProductORM.objects.filter(active=True)
        return [self._to_domain(product_orm) for product_orm in products_orm]
    
    def create(self, product: Product) -> Product:
        """
        Create a new product.
        
        Args:
            product: The product to create.
            
        Returns:
            The created product.
        """
        product_orm = ProductORM(
            uid=uuid4() if not product.uid else product.uid,
            name=product.name,
            description=product.description,
            active=product.active,
            stripe_id=product.stripe_id
        )
        product_orm.save()
        
        return self._to_domain(product_orm)
    
    def update(self, product: Product) -> Product:
        """
        Update an existing product.
        
        Args:
            product: The product to update.
            
        Returns:
            The updated product.
        """
        try:
            product_orm = ProductORM.objects.get(id=product.id)
        except ProductORM.DoesNotExist:
            raise ProductNotFoundError(product.id)
        
        product_orm.name = product.name
        product_orm.description = product.description
        product_orm.active = product.active
        product_orm.stripe_id = product.stripe_id
        product_orm.save()
        
        return self._to_domain(product_orm)
    
    def delete(self, product_id: int) -> None:
        """
        Delete a product.
        
        Args:
            product_id: The ID of the product to delete.
        """
        try:
            product_orm = ProductORM.objects.get(id=product_id)
            product_orm.delete()
        except ProductORM.DoesNotExist:
            raise ProductNotFoundError(product_id)
    
    def _to_domain(self, product_orm: ProductORM) -> Product:
        """
        Convert an ORM product to a domain product.
        
        Args:
            product_orm: The ORM product to convert.
            
        Returns:
            The domain product.
        """
        return Product(
            id=product_orm.id,
            uid=product_orm.uid,
            name=product_orm.name,
            description=product_orm.description,
            active=product_orm.active,
            stripe_id=product_orm.stripe_id,
            is_active=product_orm.is_active
        )


class PriceRepository(IPriceRepository):
    """
    Implementation of the price repository.
    """
    def get_by_id(self, price_id: int) -> Optional[Price]:
        """
        Get a price by its ID.
        
        Args:
            price_id: The ID of the price to retrieve.
            
        Returns:
            The price, or None if not found.
        """
        try:
            price_orm = PriceORM.objects.get(id=price_id)
            return self._to_domain(price_orm)
        except PriceORM.DoesNotExist:
            return None
    
    def get_by_product_id(self, product_id: int) -> List[Price]:
        """
        Get all prices for a product.
        
        Args:
            product_id: The ID of the product.
            
        Returns:
            A list of prices for the product.
        """
        prices_orm = PriceORM.objects.filter(product_id=product_id)
        return [self._to_domain(price_orm) for price_orm in prices_orm]
    
    def get_by_stripe_id(self, stripe_id: str) -> Optional[Price]:
        """
        Get a price by its Stripe ID.
        
        Args:
            stripe_id: The Stripe ID of the price.
            
        Returns:
            The price, or None if not found.
        """
        try:
            price_orm = PriceORM.objects.get(stripe_id=stripe_id)
            return self._to_domain(price_orm)
        except PriceORM.DoesNotExist:
            return None
    
    def create(self, price: Price) -> Price:
        """
        Create a new price.
        
        Args:
            price: The price to create.
            
        Returns:
            The created price.
        """
        price_orm = PriceORM(
            uid=uuid4() if not price.uid else price.uid,
            product_id=price.product_id,
            unit_amount=price.unit_amount,
            currency=price.currency,
            interval=price.interval,
            interval_count=price.interval_count,
            stripe_id=price.stripe_id
        )
        price_orm.save()
        
        return self._to_domain(price_orm)
    
    def update(self, price: Price) -> Price:
        """
        Update an existing price.
        
        Args:
            price: The price to update.
            
        Returns:
            The updated price.
        """
        try:
            price_orm = PriceORM.objects.get(id=price.id)
        except PriceORM.DoesNotExist:
            raise PriceNotFoundError(price.id)
        
        price_orm.product_id = price.product_id
        price_orm.unit_amount = price.unit_amount
        price_orm.currency = price.currency
        price_orm.interval = price.interval
        price_orm.interval_count = price.interval_count
        price_orm.stripe_id = price.stripe_id
        price_orm.save()
        
        return self._to_domain(price_orm)
    
    def delete(self, price_id: int) -> None:
        """
        Delete a price.
        
        Args:
            price_id: The ID of the price to delete.
        """
        try:
            price_orm = PriceORM.objects.get(id=price_id)
            price_orm.delete()
        except PriceORM.DoesNotExist:
            raise PriceNotFoundError(price_id)
    
    def _to_domain(self, price_orm: PriceORM) -> Price:
        """
        Convert an ORM price to a domain price.
        
        Args:
            price_orm: The ORM price to convert.
            
        Returns:
            The domain price.
        """
        return Price(
            id=price_orm.id,
            uid=price_orm.uid,
            product_id=price_orm.product_id,
            unit_amount=price_orm.unit_amount,
            currency=price_orm.currency,
            interval=price_orm.interval,
            interval_count=price_orm.interval_count,
            stripe_id=price_orm.stripe_id,
            is_active=price_orm.is_active
        )

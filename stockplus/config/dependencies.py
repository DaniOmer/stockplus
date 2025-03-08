"""
Dependency injection configuration for the application.
"""

from stockplus.modules.product.application.services import ProductService as ProductCatalogService
from stockplus.modules.product.infrastructure.repositories import ProductRepository as ProductCatalogRepository
from stockplus.modules.sales.application.services import SaleService, InvoiceService
from stockplus.modules.sales.infrastructure.repositories import SaleRepository, InvoiceRepository
from stockplus.modules.subscription.application.services import SubscriptionService
from stockplus.modules.subscription.infrastructure.repositories import (
    SubscriptionRepository,
    SubscriptionPlanRepository
)
from stockplus.modules.shop.application.services import (
    CustomerService,
    ProductService as ShopProductService,
    PriceService
)
from stockplus.modules.shop.infrastructure.repositories import (
    CustomerRepository,
    ProductRepository as ShopProductRepository,
    PriceRepository
)


def get_product_service() -> ProductCatalogService:
    """
    Get the product service.
    
    Returns:
        The product service.
    """
    product_repository = ProductCatalogRepository()
    return ProductCatalogService(product_repository)


def get_sale_service() -> SaleService:
    """
    Get the sale service.
    
    Returns:
        The sale service.
    """
    sale_repository = SaleRepository()
    invoice_repository = InvoiceRepository()
    product_service = get_product_service()
    return SaleService(sale_repository, invoice_repository, product_service)


def get_invoice_service() -> InvoiceService:
    """
    Get the invoice service.
    
    Returns:
        The invoice service.
    """
    invoice_repository = InvoiceRepository()
    return InvoiceService(invoice_repository)


def get_subscription_service() -> SubscriptionService:
    """
    Get the subscription service.
    
    Returns:
        The subscription service.
    """
    subscription_repository = SubscriptionRepository()
    subscription_plan_repository = SubscriptionPlanRepository()
    return SubscriptionService(subscription_repository, subscription_plan_repository)


def get_shop_customer_service() -> CustomerService:
    """
    Get the shop customer service.
    
    Returns:
        The shop customer service.
    """
    customer_repository = CustomerRepository()
    return CustomerService(customer_repository)


def get_shop_product_service() -> ShopProductService:
    """
    Get the shop product service.
    
    Returns:
        The shop product service.
    """
    product_repository = ShopProductRepository()
    return ShopProductService(product_repository)


def get_price_service() -> PriceService:
    """
    Get the price service.
    
    Returns:
        The price service.
    """
    price_repository = PriceRepository()
    product_repository = ShopProductRepository()
    return PriceService(price_repository, product_repository)

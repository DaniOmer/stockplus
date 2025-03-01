from stockplus.modules.pointofsale.application.services import PointOfSaleService
from stockplus.modules.pointofsale.infrastructure.repositories.repositories import DjangoPointOfSaleRepository

from stockplus.modules.product.application.services import (
    BrandService, ProductCategoryService, ProductService, PointOfSaleProductVariantService
)
from stockplus.modules.product.infrastructure.repositories import (
    DjangoBrandRepository, DjangoProductCategoryRepository, 
    DjangoProductRepository, DjangoPointOfSaleProductVariantRepository
)


# Point of Sale dependencies
def get_point_of_sale_repository():
    """
    Get the point of sale repository.
    
    Returns:
        The point of sale repository.
    """
    return DjangoPointOfSaleRepository()


def get_point_of_sale_service():
    """
    Get the point of sale service.
    
    Returns:
        The point of sale service.
    """
    repository = get_point_of_sale_repository()
    return PointOfSaleService(repository)


# Product dependencies
def get_brand_repository():
    """
    Get the brand repository.
    
    Returns:
        The brand repository.
    """
    return DjangoBrandRepository()


def get_brand_service():
    """
    Get the brand service.
    
    Returns:
        The brand service.
    """
    repository = get_brand_repository()
    return BrandService(repository)


def get_product_category_repository():
    """
    Get the product category repository.
    
    Returns:
        The product category repository.
    """
    return DjangoProductCategoryRepository()


def get_product_category_service():
    """
    Get the product category service.
    
    Returns:
        The product category service.
    """
    repository = get_product_category_repository()
    return ProductCategoryService(repository)


def get_product_repository():
    """
    Get the product repository.
    
    Returns:
        The product repository.
    """
    return DjangoProductRepository()


def get_product_service():
    """
    Get the product service.
    
    Returns:
        The product service.
    """
    repository = get_product_repository()
    brand_service = get_brand_service()
    category_service = get_product_category_service()
    return ProductService(repository, brand_service, category_service)


def get_point_of_sale_product_variant_repository():
    """
    Get the point of sale product variant repository.
    
    Returns:
        The point of sale product variant repository.
    """
    return DjangoPointOfSaleProductVariantRepository()


def get_point_of_sale_product_variant_service():
    """
    Get the point of sale product variant service.
    
    Returns:
        The point of sale product variant service.
    """
    repository = get_point_of_sale_product_variant_repository()
    return PointOfSaleProductVariantService(repository)

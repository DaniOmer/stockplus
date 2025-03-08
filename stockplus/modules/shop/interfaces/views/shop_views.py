"""
Shop views for the shop application.
This module contains the views for the shop application.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Custom throttle classes
class ShopRateThrottle(UserRateThrottle):
    rate = '10/minute'  # Limit to 10 requests per minute for authenticated users

class ShopAnonRateThrottle(AnonRateThrottle):
    rate = '3/minute'  # Limit to 3 requests per minute for anonymous users

from stockplus.modules.shop.infrastructure.models import Product, Price
from stockplus.modules.shop.interfaces.serializers import (
    ProductSerializer,
    PriceSerializer,
    CreateProductSerializer,
    CreatePriceSerializer
)
from stockplus.modules.shop.application.services import (
    ProductService,
    PriceService
)
from stockplus.modules.shop.domain.exceptions import (
    ProductNotFoundError,
    PriceNotFoundError,
    ProductAlreadyExistsError,
    StripeError
)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage products.
    """
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ShopRateThrottle]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = None
    
    def get_product_service(self) -> ProductService:
        """
        Get the product service from the dependency container.
        
        Returns:
            The product service.
        """
        if not self.product_service:
            from stockplus.config.dependencies import get_product_service
            self.product_service = get_product_service()
        return self.product_service
    
    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action == 'create_product':
            return CreateProductSerializer
        return ProductSerializer
    
    def list(self, request):
        """
        Get all active products.
        """
        service = self.get_product_service()
        products = service.get_all_active_products()
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        Get a product by ID.
        """
        service = self.get_product_service()
        
        try:
            product = service.get_product(pk)
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        except ProductNotFoundError:
            return Response({
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def create_product(self, request):
        """
        Create a new product.
        """
        name = request.data.get('name')
        description = request.data.get('description')
        active = request.data.get('active', True)
        
        if not name:
            return Response({
                'message': 'Name is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        service = self.get_product_service()
        
        try:
            product = service.create_product(name, description, active)
            serializer = ProductSerializer(product)
            return Response({
                'message': 'Product created successfully',
                'product': serializer.data
            }, status=status.HTTP_201_CREATED)
        except ProductAlreadyExistsError:
            return Response({
                'message': f'Product with name "{name}" already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        except StripeError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """
        Update a product.
        """
        service = self.get_product_service()
        
        try:
            # Get the product
            product = service.get_product(pk)
            
            # Update the product
            product.name = request.data.get('name', product.name)
            product.description = request.data.get('description', product.description)
            product.active = request.data.get('active', product.active)
            
            # Save the product
            updated_product = service.update_product(product)
            
            serializer = self.get_serializer(updated_product)
            return Response({
                'message': 'Product updated successfully',
                'product': serializer.data
            })
        except ProductNotFoundError:
            return Response({
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except StripeError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Delete a product.
        """
        service = self.get_product_service()
        
        try:
            service.delete_product(pk)
            return Response({
                'message': 'Product deleted successfully'
            })
        except ProductNotFoundError:
            return Response({
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except StripeError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class PriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage prices.
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ShopRateThrottle]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.price_service = None
    
    def get_price_service(self) -> PriceService:
        """
        Get the price service from the dependency container.
        
        Returns:
            The price service.
        """
        if not self.price_service:
            from stockplus.config.dependencies import get_price_service
            self.price_service = get_price_service()
        return self.price_service
    
    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action == 'create_price':
            return CreatePriceSerializer
        return PriceSerializer
    
    def list(self, request):
        """
        Get all prices.
        """
        product_id = request.query_params.get('product_id')
        
        if product_id:
            service = self.get_price_service()
            prices = service.get_prices_by_product_id(product_id)
            
            serializer = self.get_serializer(prices, many=True)
            return Response(serializer.data)
        
        return super().list(request)
    
    def retrieve(self, request, pk=None):
        """
        Get a price by ID.
        """
        service = self.get_price_service()
        
        try:
            price = service.get_price(pk)
            serializer = self.get_serializer(price)
            return Response(serializer.data)
        except PriceNotFoundError:
            return Response({
                'message': 'Price not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def create_price(self, request):
        """
        Create a new price.
        """
        product_id = request.data.get('product_id')
        unit_amount = request.data.get('unit_amount')
        currency = request.data.get('currency', 'eur')
        interval = request.data.get('interval')
        interval_count = request.data.get('interval_count')
        
        if not product_id:
            return Response({
                'message': 'Product ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not unit_amount:
            return Response({
                'message': 'Unit amount is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        service = self.get_price_service()
        
        try:
            price = service.create_price(
                product_id=product_id,
                unit_amount=unit_amount,
                currency=currency,
                interval=interval,
                interval_count=interval_count
            )
            
            serializer = PriceSerializer(price)
            return Response({
                'message': 'Price created successfully',
                'price': serializer.data
            }, status=status.HTTP_201_CREATED)
        except ProductNotFoundError:
            return Response({
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except StripeError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """
        Update a price.
        """
        service = self.get_price_service()
        
        try:
            # Get the price
            price = service.get_price(pk)
            
            # Update the price
            price.product_id = request.data.get('product_id', price.product_id)
            price.unit_amount = request.data.get('unit_amount', price.unit_amount)
            price.currency = request.data.get('currency', price.currency)
            price.interval = request.data.get('interval', price.interval)
            price.interval_count = request.data.get('interval_count', price.interval_count)
            
            # Save the price
            updated_price = service.update_price(price)
            
            serializer = self.get_serializer(updated_price)
            return Response({
                'message': 'Price updated successfully',
                'price': serializer.data
            })
        except PriceNotFoundError:
            return Response({
                'message': 'Price not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except ProductNotFoundError:
            return Response({
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except StripeError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        """
        Delete a price.
        """
        service = self.get_price_service()
        
        try:
            service.delete_price(pk)
            return Response({
                'message': 'Price deleted successfully'
            })
        except PriceNotFoundError:
            return Response({
                'message': 'Price not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except StripeError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

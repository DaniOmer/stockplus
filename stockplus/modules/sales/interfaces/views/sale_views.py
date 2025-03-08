from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from stockplus.modules.sales.application.services import SaleService
from stockplus.modules.sales.domain.exceptions import (
    SaleNotFoundError, SaleItemNotFoundError, 
    SaleAlreadyCancelledError, InsufficientStockError
)
from stockplus.modules.sales.infrastructure.models import Sale as SaleORM
from stockplus.modules.sales.interfaces.serializers import SaleSerializer, SaleItemSerializer


class SaleViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing sales.
    """
    queryset = SaleORM.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date', 'payment_method', 'point_of_sale', 'is_cancelled']
    search_fields = ['invoice_number', 'notes']
    ordering_fields = ['date', 'total_amount']
    ordering = ['-date']
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sale_service = None
    
    def get_sale_service(self) -> SaleService:
        """
        Get the sale service from the dependency container.
        
        Returns:
            The sale service.
        """
        if not self.sale_service:
            from stockplus.config.dependencies import get_sale_service
            self.sale_service = get_sale_service()
        return self.sale_service
    
    def get_queryset(self):
        """
        Get the queryset for the view.
        
        Returns:
            The queryset.
        """
        company = self.request.user.company
        if not company:
            return SaleORM.objects.none()
        
        queryset = SaleORM.objects.filter(company=company)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # Filter by product
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(sale_items__product_id=product_id).distinct()
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Create a new sale.
        
        Returns:
            Response with the created sale.
        """
        # Extract items from request data
        items_data = request.data.pop('items', [])
        
        # Create serializer for the sale
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the sale service
        service = self.get_sale_service()
        
        try:
            # Create the sale
            sale = service.create_sale(
                company_id=request.user.company.id,
                items=[{
                    'product_id': item.get('product_id'),
                    'product_variant_id': item.get('product_variant_id'),
                    'quantity': item.get('quantity', 1),
                    'unit_price': item.get('unit_price', 0),
                    'discount': item.get('discount', 0)
                } for item in items_data],
                payment_method=serializer.validated_data.get('payment_method', 'cash'),
                point_of_sale_id=serializer.validated_data.get('point_of_sale').id if 'point_of_sale' in serializer.validated_data else None,
                user_id=request.user.id,
                notes=serializer.validated_data.get('notes'),
                customer_name=request.data.get('customer_name'),
                customer_email=request.data.get('customer_email'),
                customer_phone=request.data.get('customer_phone'),
                customer_address=request.data.get('customer_address')
            )
            
            # Get the ORM sale to return
            orm_sale = SaleORM.objects.get(id=sale.id)
            result_serializer = self.get_serializer(orm_sale)
            
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        except InsufficientStockError as e:
            return Response({
                'detail': str(e),
                'product_id': e.product_id,
                'requested': e.requested,
                'available': e.available
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel a sale.
        
        Returns:
            Response with the cancelled sale.
        """
        # Get the sale service
        service = self.get_sale_service()
        
        try:
            # Cancel the sale
            sale = service.cancel_sale(
                sale_id=pk,
                user_id=request.user.id
            )
            
            # Get the ORM sale to return
            orm_sale = SaleORM.objects.get(id=sale.id)
            serializer = self.get_serializer(orm_sale)
            
            return Response(serializer.data)
        except SaleNotFoundError:
            return Response({'detail': 'Sale not found.'}, status=status.HTTP_404_NOT_FOUND)
        except SaleAlreadyCancelledError:
            return Response({'detail': 'Sale is already cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """
        Add an item to a sale.
        
        Returns:
            Response with the added item.
        """
        # Create serializer for the item
        serializer = SaleItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the sale service
        service = self.get_sale_service()
        
        try:
            # Add the item to the sale
            item = service.add_item_to_sale(
                sale_id=pk,
                product_id=serializer.validated_data.get('product').id,
                quantity=serializer.validated_data.get('quantity', 1),
                product_variant_id=serializer.validated_data.get('product_variant').id if 'product_variant' in serializer.validated_data else None,
                unit_price=serializer.validated_data.get('unit_price'),
                discount=serializer.validated_data.get('discount', 0)
            )
            
            # Return the updated sale
            orm_sale = SaleORM.objects.get(id=pk)
            sale_serializer = self.get_serializer(orm_sale)
            
            return Response(sale_serializer.data)
        except SaleNotFoundError:
            return Response({'detail': 'Sale not found.'}, status=status.HTTP_404_NOT_FOUND)
        except InsufficientStockError as e:
            return Response({
                'detail': str(e),
                'product_id': e.product_id,
                'requested': e.requested,
                'available': e.available
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='remove-item/(?P<item_id>[^/.]+)')
    def remove_item(self, request, pk=None, item_id=None):
        """
        Remove an item from a sale.
        
        Returns:
            Response with the updated sale.
        """
        # Get the sale service
        service = self.get_sale_service()
        
        try:
            # Remove the item from the sale
            service.remove_sale_item(item_id=item_id)
            
            # Return the updated sale
            orm_sale = SaleORM.objects.get(id=pk)
            serializer = self.get_serializer(orm_sale)
            
            return Response(serializer.data)
        except SaleNotFoundError:
            return Response({'detail': 'Sale not found.'}, status=status.HTTP_404_NOT_FOUND)
        except SaleItemNotFoundError:
            return Response({'detail': 'Sale item not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from stockplus.modules.sales.application.services import InvoiceService
from stockplus.modules.sales.domain.exceptions import InvoiceNotFoundError
from stockplus.modules.sales.infrastructure.models import Invoice as InvoiceORM
from stockplus.modules.sales.interfaces.serializers import InvoiceSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing invoices.
    """
    queryset = InvoiceORM.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date', 'is_paid', 'sale']
    search_fields = ['invoice_number', 'customer_name', 'customer_email', 'notes']
    ordering_fields = ['date', 'total_amount', 'due_date']
    ordering = ['-date']
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invoice_service = None
    
    def get_invoice_service(self) -> InvoiceService:
        """
        Get the invoice service from the dependency container.
        
        Returns:
            The invoice service.
        """
        if not self.invoice_service:
            from stockplus.config.dependencies import get_invoice_service
            self.invoice_service = get_invoice_service()
        return self.invoice_service
    
    def get_queryset(self):
        """
        Get the queryset for the view.
        
        Returns:
            The queryset.
        """
        company = self.request.user.company
        if not company:
            return InvoiceORM.objects.none()
        
        queryset = InvoiceORM.objects.filter(company=company)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    
    def update(self, request, *args, **kwargs):
        """
        Update an existing invoice.
        
        Returns:
            Response with the updated invoice.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Get the invoice service
        service = self.get_invoice_service()
        
        try:
            # Update the invoice
            invoice = service.update_invoice(
                invoice_id=instance.id,
                due_date=serializer.validated_data.get('due_date'),
                tax_amount=serializer.validated_data.get('tax_amount'),
                discount_amount=serializer.validated_data.get('discount_amount'),
                customer_name=serializer.validated_data.get('customer_name'),
                customer_email=serializer.validated_data.get('customer_email'),
                customer_phone=serializer.validated_data.get('customer_phone'),
                customer_address=serializer.validated_data.get('customer_address'),
                notes=serializer.validated_data.get('notes')
            )
            
            # Get the ORM invoice to return
            orm_invoice = InvoiceORM.objects.get(id=invoice.id)
            result_serializer = self.get_serializer(orm_invoice)
            
            return Response(result_serializer.data)
        except InvoiceNotFoundError:
            return Response({'detail': 'Invoice not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        """
        Mark an invoice as paid.
        
        Returns:
            Response with the updated invoice.
        """
        # Get the invoice service
        service = self.get_invoice_service()
        
        try:
            # Mark the invoice as paid
            invoice = service.mark_as_paid(invoice_id=pk)
            
            # Get the ORM invoice to return
            orm_invoice = InvoiceORM.objects.get(id=invoice.id)
            serializer = self.get_serializer(orm_invoice)
            
            return Response(serializer.data)
        except InvoiceNotFoundError:
            return Response({'detail': 'Invoice not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def generate_pdf(self, request, pk=None):
        """
        Generate a PDF for an invoice.
        
        Returns:
            Response with the path to the generated PDF.
        """
        # Get the invoice service
        service = self.get_invoice_service()
        
        try:
            # Generate the PDF
            pdf_path = service.generate_pdf(invoice_id=pk)
            
            if pdf_path:
                return Response({'pdf_path': pdf_path})
            else:
                return Response({'detail': 'Failed to generate PDF.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except InvoiceNotFoundError:
            return Response({'detail': 'Invoice not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

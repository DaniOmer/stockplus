"""
Report views.
This module contains the views for the reports module.
"""

from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from stockplus.modules.collaborator.permissions import CanViewReports, CanExportData
from stockplus.modules.reports.interfaces.serializers import (
    SalesReportSerializer,
    InventoryReportSerializer,
    ProductReportSerializer,
    ExportDataSerializer,
    DashboardDataSerializer,
)
from stockplus.config.dependencies import (
    get_report_service,
    get_export_service,
    get_dashboard_service,
)


class SalesReportView(views.APIView):
    """
    View for generating sales reports.
    """
    permission_classes = [IsAuthenticated, CanViewReports]
    
    def post(self, request):
        """
        Generate a sales report.
        """
        serializer = SalesReportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated data
        data = serializer.validated_data
        
        # Get report service
        report_service = get_report_service()
        
        # Generate report
        report = report_service.generate_sales_report(
            company_id=request.user.company_id,
            start_date=data['start_date'],
            end_date=data['end_date'],
            pos_id=data.get('pos_id')
        )
        
        return Response(report)


class InventoryReportView(views.APIView):
    """
    View for generating inventory reports.
    """
    permission_classes = [IsAuthenticated, CanViewReports]
    
    def post(self, request):
        """
        Generate an inventory report.
        """
        serializer = InventoryReportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated data
        data = serializer.validated_data
        
        # Get report service
        report_service = get_report_service()
        
        # Generate report
        report = report_service.generate_inventory_report(
            company_id=request.user.company_id,
            pos_id=data.get('pos_id'),
            low_stock_threshold=data.get('low_stock_threshold')
        )
        
        return Response(report)


class ProductReportView(views.APIView):
    """
    View for generating product reports.
    """
    permission_classes = [IsAuthenticated, CanViewReports]
    
    def post(self, request):
        """
        Generate a product report.
        """
        serializer = ProductReportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated data
        data = serializer.validated_data
        
        # Get report service
        report_service = get_report_service()
        
        # Generate report
        report = report_service.generate_product_report(
            company_id=request.user.company_id,
            start_date=data['start_date'],
            end_date=data['end_date'],
            pos_id=data.get('pos_id')
        )
        
        return Response(report)


class ExportDataView(views.APIView):
    """
    View for exporting data.
    """
    permission_classes = [IsAuthenticated, CanExportData]
    
    def post(self, request):
        """
        Export data.
        """
        serializer = ExportDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated data
        data = serializer.validated_data
        
        # Get export service
        export_service = get_export_service()
        
        # Export data
        export_type = data['export_type']
        export_format = data.get('format', 'csv')
        
        if export_type == 'sales':
            # Export sales data
            export_data = export_service.export_sales_data(
                company_id=request.user.company_id,
                start_date=data['start_date'],
                end_date=data['end_date'],
                format=export_format,
                pos_id=data.get('pos_id')
            )
        elif export_type == 'inventory':
            # Export inventory data
            export_data = export_service.export_inventory_data(
                company_id=request.user.company_id,
                format=export_format,
                pos_id=data.get('pos_id')
            )
        elif export_type == 'products':
            # Export product data
            export_data = export_service.export_product_data(
                company_id=request.user.company_id,
                format=export_format,
                pos_id=data.get('pos_id')
            )
        else:
            return Response(
                {'error': _('Invalid export type')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set content type and filename
        if export_format == 'csv':
            content_type = 'text/csv'
            filename = f'{export_type}_export.csv'
        elif export_format == 'excel':
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            filename = f'{export_type}_export.xlsx'
        elif export_format == 'pdf':
            content_type = 'application/pdf'
            filename = f'{export_type}_export.pdf'
        else:
            content_type = 'application/octet-stream'
            filename = f'{export_type}_export'
        
        # Create response
        response = HttpResponse(export_data, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response


class DashboardView(views.APIView):
    """
    View for getting dashboard data.
    """
    permission_classes = [IsAuthenticated, CanViewReports]
    
    def post(self, request):
        """
        Get dashboard data.
        """
        serializer = DashboardDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated data
        data = serializer.validated_data
        
        # Get dashboard service
        dashboard_service = get_dashboard_service()
        
        # Get dashboard data
        dashboard_data = dashboard_service.get_dashboard_data(
            company_id=request.user.company_id,
            pos_id=data.get('pos_id')
        )
        
        return Response(dashboard_data)

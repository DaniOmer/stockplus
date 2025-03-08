"""
Export service implementation.
This module contains the implementation of the export service.
"""

import csv
import io
from typing import Dict, Any, Optional, List
from datetime import date, datetime
from django.db.models import Sum, Count, F, Q, Avg
from django.utils.translation import gettext_lazy as _

from stockplus.modules.reports.application.interfaces import ExportServiceInterface
from stockplus.modules.sales.infrastructure.models import Sale
from stockplus.modules.product.infrastructure.models import Product

try:
    import xlsxwriter
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class ExportService(ExportServiceInterface):
    """
    Implementation of the export service.
    """
    
    def export_sales_data(
        self, 
        company_id: int, 
        start_date: date, 
        end_date: date, 
        format: str = 'csv',
        pos_id: Optional[int] = None
    ) -> io.BytesIO:
        """
        Export sales data for a specific period.
        
        Args:
            company_id: The ID of the company.
            start_date: The start date of the period.
            end_date: The end date of the period.
            format: The export format ('csv', 'excel', or 'pdf').
            pos_id: Optional point of sale ID to filter by.
            
        Returns:
            A BytesIO object containing the exported data.
        """
        # Convert dates to datetime for filtering
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        # Base query for sales
        sales_query = Sale.objects.filter(
            company_id=company_id,
            date__gte=start_datetime,
            date__lte=end_datetime,
            is_cancelled=False
        ).select_related('point_of_sale', 'user')
        
        # Filter by point of sale if provided
        if pos_id:
            sales_query = sales_query.filter(point_of_sale_id=pos_id)
        
        # Prepare data for export
        header = [
            _('Invoice Number'),
            _('Date'),
            _('Total Amount'),
            _('Payment Method'),
            _('Point of Sale'),
            _('Cashier'),
            _('Items Count'),
        ]
        
        data = []
        for sale in sales_query:
            data.append([
                sale.invoice_number or '',
                sale.date.strftime('%Y-%m-%d %H:%M:%S'),
                str(sale.total_amount),
                sale.get_payment_method_display(),
                sale.point_of_sale.name if sale.point_of_sale else '',
                str(sale.user) if sale.user else '',
                sale.item_count,
            ])
        
        # Export data in the requested format
        if format == 'excel' and EXCEL_AVAILABLE:
            return self._export_to_excel(header, data, _('Sales Report'))
        elif format == 'pdf' and PDF_AVAILABLE:
            return self._export_to_pdf(header, data, _('Sales Report'))
        else:
            return self._export_to_csv(header, data)
    
    def export_inventory_data(
        self, 
        company_id: int, 
        format: str = 'csv',
        pos_id: Optional[int] = None
    ) -> io.BytesIO:
        """
        Export inventory data.
        
        Args:
            company_id: The ID of the company.
            format: The export format ('csv', 'excel', or 'pdf').
            pos_id: Optional point of sale ID to filter by.
            
        Returns:
            A BytesIO object containing the exported data.
        """
        # Base query for product stock
        stock_query = Product.objects.filter(
            product__company_id=company_id
        ).select_related('product', 'point_of_sale')
        
        # Filter by point of sale if provided
        if pos_id:
            stock_query = stock_query.filter(point_of_sale_id=pos_id)
        
        # Prepare data for export
        header = [
            _('Product ID'),
            _('Product Name'),
            _('SKU'),
            _('Category'),
            _('Point of Sale'),
            _('Quantity'),
            _('Price'),
            _('Value'),
        ]
        
        data = []
        for stock in stock_query:
            data.append([
                stock.product.id,
                stock.product.name,
                stock.product.sku or '',
                stock.product.category.name if stock.product.category else '',
                stock.point_of_sale.name if stock.point_of_sale else '',
                stock.quantity,
                str(stock.product.price),
                str(stock.quantity * stock.product.price),
            ])
        
        # Export data in the requested format
        if format == 'excel' and EXCEL_AVAILABLE:
            return self._export_to_excel(header, data, _('Inventory Report'))
        elif format == 'pdf' and PDF_AVAILABLE:
            return self._export_to_pdf(header, data, _('Inventory Report'))
        else:
            return self._export_to_csv(header, data)
    
    def export_product_data(
        self, 
        company_id: int, 
        format: str = 'csv',
        pos_id: Optional[int] = None
    ) -> io.BytesIO:
        """
        Export product data.
        
        Args:
            company_id: The ID of the company.
            format: The export format ('csv', 'excel', or 'pdf').
            pos_id: Optional point of sale ID to filter by.
            
        Returns:
            A BytesIO object containing the exported data.
        """
        # Base query for products
        products_query = Product.objects.filter(
            company_id=company_id
        ).select_related('category')
        
        # Prepare data for export
        header = [
            _('Product ID'),
            _('Product Name'),
            _('SKU'),
            _('Category'),
            _('Description'),
            _('Price'),
            _('Active'),
        ]
        
        data = []
        for product in products_query:
            data.append([
                product.id,
                product.name,
                product.sku or '',
                product.category.name if product.category else '',
                product.description or '',
                str(product.price),
                _('Yes') if not product.is_disable else _('No'),
            ])
        
        # Export data in the requested format
        if format == 'excel' and EXCEL_AVAILABLE:
            return self._export_to_excel(header, data, _('Products Report'))
        elif format == 'pdf' and PDF_AVAILABLE:
            return self._export_to_pdf(header, data, _('Products Report'))
        else:
            return self._export_to_csv(header, data)
    
    def _export_to_csv(self, header: List[str], data: List[List[Any]]) -> io.BytesIO:
        """
        Export data to CSV format.
        
        Args:
            header: The header row.
            data: The data rows.
            
        Returns:
            A BytesIO object containing the CSV data.
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(header)
        
        # Write data
        for row in data:
            writer.writerow(row)
        
        # Convert to bytes
        csv_data = output.getvalue().encode('utf-8')
        
        # Create BytesIO object
        bytes_io = io.BytesIO()
        bytes_io.write(csv_data)
        bytes_io.seek(0)
        
        return bytes_io
    
    def _export_to_excel(self, header: List[str], data: List[List[Any]], title: str) -> io.BytesIO:
        """
        Export data to Excel format.
        
        Args:
            header: The header row.
            data: The data rows.
            title: The title of the report.
            
        Returns:
            A BytesIO object containing the Excel data.
        """
        if not EXCEL_AVAILABLE:
            raise ImportError("xlsxwriter is required for Excel export")
        
        # Create BytesIO object
        output = io.BytesIO()
        
        # Create workbook and worksheet
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Add title
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
        })
        worksheet.write(0, 0, title, title_format)
        
        # Add header
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#CCCCCC',
            'border': 1,
        })
        for col, value in enumerate(header):
            worksheet.write(2, col, value, header_format)
        
        # Add data
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                worksheet.write(row_idx + 3, col_idx, value)
        
        # Auto-fit columns
        for col_idx, _ in enumerate(header):
            worksheet.set_column(col_idx, col_idx, 15)
        
        # Close workbook
        workbook.close()
        
        # Reset file pointer
        output.seek(0)
        
        return output
    
    def _export_to_pdf(self, header: List[str], data: List[List[Any]], title: str) -> io.BytesIO:
        """
        Export data to PDF format.
        
        Args:
            header: The header row.
            data: The data rows.
            title: The title of the report.
            
        Returns:
            A BytesIO object containing the PDF data.
        """
        if not PDF_AVAILABLE:
            raise ImportError("reportlab is required for PDF export")
        
        # Create BytesIO object
        output = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output,
            pagesize=landscape(letter),
            title=title,
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        
        # Create elements
        elements = []
        
        # Add title
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 12))
        
        # Add table
        table_data = [header] + data
        table = Table(table_data)
        
        # Add table style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)
        
        # Add table to elements
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        # Reset file pointer
        output.seek(0)
        
        return output

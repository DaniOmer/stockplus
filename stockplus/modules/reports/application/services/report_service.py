"""
Report service implementation.
This module contains the implementation of the report service.
"""

from typing import Dict, Any, Optional, List
from datetime import date, datetime, timedelta
from django.db.models import Sum, Count, F, Q, Avg
from django.db.models.functions import TruncDay, TruncMonth

from stockplus.modules.reports.application.interfaces import ReportServiceInterface
from stockplus.modules.sales.infrastructure.models import Sale, SaleItem
from stockplus.modules.product.infrastructure.models import Product


class ReportService(ReportServiceInterface):
    """
    Implementation of the report service.
    """
    
    def generate_sales_report(
        self, 
        company_id: int, 
        start_date: date, 
        end_date: date, 
        pos_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a sales report for a specific period.
        
        Args:
            company_id: The ID of the company.
            start_date: The start date of the period.
            end_date: The end date of the period.
            pos_id: Optional point of sale ID to filter by.
            
        Returns:
            A dictionary containing the sales report data.
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
        )
        
        # Filter by point of sale if provided
        if pos_id:
            sales_query = sales_query.filter(point_of_sale_id=pos_id)
        
        # Calculate sales metrics
        total_sales = sales_query.count()
        total_revenue = sales_query.aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Calculate average sale value
        avg_sale_value = 0
        if total_sales > 0:
            avg_sale_value = total_revenue / total_sales
        
        # Calculate sales by payment method
        sales_by_payment_method = sales_query.values('payment_method').annotate(
            count=Count('id'),
            total=Sum('total_amount')
        ).order_by('-total')
        
        # Calculate sales by day
        sales_by_day = sales_query.annotate(
            day=TruncDay('date')
        ).values('day').annotate(
            count=Count('id'),
            total=Sum('total_amount')
        ).order_by('day')
        
        # Calculate sales by product category
        sales_by_category = SaleItem.objects.filter(
            sale__in=sales_query
        ).values(
            'product__category__name'
        ).annotate(
            count=Count('id'),
            total=Sum('total_price')
        ).order_by('-total')
        
        # Calculate top selling products
        top_products = SaleItem.objects.filter(
            sale__in=sales_query
        ).values(
            'product_id', 'product__name', 'product__sku'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_price')
        ).order_by('-total_quantity')[:10]
        
        # Return the sales report data
        return {
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'days': (end_date - start_date).days + 1,
            },
            'summary': {
                'total_sales': total_sales,
                'total_revenue': float(total_revenue),
                'avg_sale_value': float(avg_sale_value),
            },
            'payment_methods': [
                {
                    'method': item['payment_method'],
                    'count': item['count'],
                    'total': float(item['total']),
                    'percentage': float(item['total'] / total_revenue * 100) if total_revenue > 0 else 0,
                }
                for item in sales_by_payment_method
            ],
            'daily_sales': [
                {
                    'date': item['day'].isoformat(),
                    'count': item['count'],
                    'total': float(item['total']),
                }
                for item in sales_by_day
            ],
            'categories': [
                {
                    'category': item['product__category__name'] or 'Uncategorized',
                    'count': item['count'],
                    'total': float(item['total']),
                    'percentage': float(item['total'] / total_revenue * 100) if total_revenue > 0 else 0,
                }
                for item in sales_by_category
            ],
            'top_products': [
                {
                    'product_id': item['product_id'],
                    'product_name': item['product__name'],
                    'product_sku': item['product__sku'] or '',
                    'total_quantity': item['total_quantity'],
                    'total_revenue': float(item['total_revenue']),
                }
                for item in top_products
            ],
        }
    
    def generate_inventory_report(
        self, 
        company_id: int, 
        pos_id: Optional[int] = None,
        low_stock_threshold: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate an inventory report.
        
        Args:
            company_id: The ID of the company.
            pos_id: Optional point of sale ID to filter by.
            low_stock_threshold: Optional threshold for low stock items.
            
        Returns:
            A dictionary containing the inventory report data.
        """
        # Set default low stock threshold if not provided
        if low_stock_threshold is None:
            low_stock_threshold = 5
        
        # Base query for product stock
        stock_query = Product.objects.filter(
            product__company_id=company_id
        )
        
        # Filter by point of sale if provided
        if pos_id:
            stock_query = stock_query.filter(point_of_sale_id=pos_id)
        
        # Calculate inventory metrics
        total_products = Product.objects.filter(company_id=company_id).count()
        total_stock_value = stock_query.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0
        
        # Get low stock items
        low_stock_items = stock_query.filter(
            quantity__lte=low_stock_threshold,
            quantity__gt=0
        ).select_related('product', 'point_of_sale')
        
        # Get out of stock items
        out_of_stock_items = stock_query.filter(
            quantity=0
        ).select_related('product', 'point_of_sale')
        
        # Get stock by category
        stock_by_category = stock_query.values(
            'product__category__name'
        ).annotate(
            count=Count('id'),
            total_quantity=Sum('quantity'),
            total_value=Sum(F('quantity') * F('product__price'))
        ).order_by('-total_value')
        
        # Return the inventory report data
        return {
            'summary': {
                'total_products': total_products,
                'total_stock_value': float(total_stock_value),
                'low_stock_count': low_stock_items.count(),
                'out_of_stock_count': out_of_stock_items.count(),
            },
            'low_stock_items': [
                {
                    'product_id': item.product.id,
                    'product_name': item.product.name,
                    'product_sku': item.product.sku or '',
                    'quantity': item.quantity,
                    'point_of_sale': item.point_of_sale.name if item.point_of_sale else '',
                    'value': float(item.quantity * item.product.price),
                }
                for item in low_stock_items
            ],
            'out_of_stock_items': [
                {
                    'product_id': item.product.id,
                    'product_name': item.product.name,
                    'product_sku': item.product.sku or '',
                    'point_of_sale': item.point_of_sale.name if item.point_of_sale else '',
                }
                for item in out_of_stock_items
            ],
            'categories': [
                {
                    'category': item['product__category__name'] or 'Uncategorized',
                    'count': item['count'],
                    'total_quantity': item['total_quantity'],
                    'total_value': float(item['total_value']),
                    'percentage': float(item['total_value'] / total_stock_value * 100) if total_stock_value > 0 else 0,
                }
                for item in stock_by_category
            ],
        }
    
    def generate_product_report(
        self, 
        company_id: int, 
        start_date: date, 
        end_date: date, 
        pos_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a product performance report for a specific period.
        
        Args:
            company_id: The ID of the company.
            start_date: The start date of the period.
            end_date: The end date of the period.
            pos_id: Optional point of sale ID to filter by.
            
        Returns:
            A dictionary containing the product report data.
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
        )
        
        # Filter by point of sale if provided
        if pos_id:
            sales_query = sales_query.filter(point_of_sale_id=pos_id)
        
        # Base query for sale items
        sale_items_query = SaleItem.objects.filter(sale__in=sales_query)
        
        # Calculate product metrics
        total_products_sold = sale_items_query.aggregate(total=Sum('quantity'))['total'] or 0
        total_revenue = sale_items_query.aggregate(total=Sum('total_price'))['total'] or 0
        
        # Calculate product performance
        product_performance = sale_items_query.values(
            'product_id', 'product__name', 'product__sku', 'product__category__name'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_price'),
            avg_price=Avg('price')
        ).order_by('-total_revenue')
        
        # Calculate product performance by day
        product_performance_by_day = sale_items_query.annotate(
            day=TruncDay('sale__date')
        ).values('day').annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_price')
        ).order_by('day')
        
        # Return the product report data
        return {
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'days': (end_date - start_date).days + 1,
            },
            'summary': {
                'total_products_sold': total_products_sold,
                'total_revenue': float(total_revenue),
                'unique_products': product_performance.count(),
            },
            'products': [
                {
                    'product_id': item['product_id'],
                    'product_name': item['product__name'],
                    'product_sku': item['product__sku'] or '',
                    'category': item['product__category__name'] or 'Uncategorized',
                    'total_quantity': item['total_quantity'],
                    'total_revenue': float(item['total_revenue']),
                    'avg_price': float(item['avg_price']),
                    'percentage': float(item['total_revenue'] / total_revenue * 100) if total_revenue > 0 else 0,
                }
                for item in product_performance
            ],
            'daily_performance': [
                {
                    'date': item['day'].isoformat(),
                    'total_quantity': item['total_quantity'],
                    'total_revenue': float(item['total_revenue']),
                }
                for item in product_performance_by_day
            ],
        }

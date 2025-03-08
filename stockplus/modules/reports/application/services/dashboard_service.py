"""
Dashboard service implementation.
This module contains the implementation of the dashboard service.
"""

from typing import Dict, Any, Optional
from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone

from stockplus.modules.reports.application.interfaces import DashboardServiceInterface
from stockplus.modules.sales.infrastructure.models import Sale, SaleItem
from stockplus.modules.product.infrastructure.models import Product


class DashboardService(DashboardServiceInterface):
    """
    Implementation of the dashboard service.
    """
    
    def get_dashboard_data(
        self, 
        company_id: int, 
        pos_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get dashboard data with key performance indicators.
        
        Args:
            company_id: The ID of the company.
            pos_id: Optional point of sale ID to filter by.
            
        Returns:
            A dictionary containing the dashboard data.
        """
        # Get current date and time
        now = timezone.now()
        today = now.date()
        yesterday = today - timedelta(days=1)
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)
        
        # Base query for sales
        sales_query = Sale.objects.filter(
            company_id=company_id,
            is_cancelled=False
        )
        
        # Filter by point of sale if provided
        if pos_id:
            sales_query = sales_query.filter(point_of_sale_id=pos_id)
        
        # Get today's sales
        today_sales = sales_query.filter(
            date__date=today
        )
        today_sales_count = today_sales.count()
        today_revenue = today_sales.aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Get yesterday's sales for comparison
        yesterday_sales = sales_query.filter(
            date__date=yesterday
        )
        yesterday_revenue = yesterday_sales.aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Calculate revenue change percentage
        revenue_change = 0
        if yesterday_revenue > 0:
            revenue_change = ((today_revenue - yesterday_revenue) / yesterday_revenue) * 100
        
        # Get weekly sales
        weekly_sales = sales_query.filter(
            date__date__gte=start_of_week,
            date__date__lte=today
        )
        weekly_revenue = weekly_sales.aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Get monthly sales
        monthly_sales = sales_query.filter(
            date__date__gte=start_of_month,
            date__date__lte=today
        )
        monthly_revenue = monthly_sales.aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Get daily sales for the last 7 days
        daily_sales = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            day_sales = sales_query.filter(date__date=day)
            day_count = day_sales.count()
            day_revenue = day_sales.aggregate(total=Sum('total_amount'))['total'] or 0
            daily_sales.append({
                'date': day.isoformat(),
                'count': day_count,
                'revenue': float(day_revenue),
            })
        
        # Get top selling products for today
        top_products = SaleItem.objects.filter(
            sale__in=today_sales
        ).values(
            'product_id', 'product__name'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum('total_price')
        ).order_by('-total_quantity')[:5]
        
        # Get low stock items
        low_stock_threshold = 5
        low_stock_items = Product.objects.filter(
            product__company_id=company_id,
            quantity__lte=low_stock_threshold,
            quantity__gt=0
        )
        if pos_id:
            low_stock_items = low_stock_items.filter(point_of_sale_id=pos_id)
        
        low_stock_count = low_stock_items.count()
        
        # Get out of stock items
        out_of_stock_items = Product.objects.filter(
            product__company_id=company_id,
            quantity=0
        )
        if pos_id:
            out_of_stock_items = out_of_stock_items.filter(point_of_sale_id=pos_id)
        
        out_of_stock_count = out_of_stock_items.count()
        
        # Get average sale value
        avg_sale_value = 0
        if today_sales_count > 0:
            avg_sale_value = today_revenue / today_sales_count
        
        # Return dashboard data
        return {
            'today': {
                'date': today.isoformat(),
                'sales_count': today_sales_count,
                'revenue': float(today_revenue),
                'avg_sale_value': float(avg_sale_value),
                'revenue_change': float(revenue_change),
            },
            'weekly': {
                'start_date': start_of_week.isoformat(),
                'end_date': today.isoformat(),
                'revenue': float(weekly_revenue),
            },
            'monthly': {
                'start_date': start_of_month.isoformat(),
                'end_date': today.isoformat(),
                'revenue': float(monthly_revenue),
            },
            'daily_sales': daily_sales,
            'top_products': [
                {
                    'product_id': item['product_id'],
                    'product_name': item['product__name'],
                    'total_quantity': item['total_quantity'],
                    'total_revenue': float(item['total_revenue']),
                }
                for item in top_products
            ],
            'inventory': {
                'low_stock_count': low_stock_count,
                'out_of_stock_count': out_of_stock_count,
            },
        }

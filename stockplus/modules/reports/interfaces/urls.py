"""
Reports URLs.
This module contains the URL patterns for the reports module.
"""

from django.urls import path

from stockplus.modules.reports.interfaces.views import (
    SalesReportView,
    InventoryReportView,
    ProductReportView,
    ExportDataView,
    DashboardView,
)

urlpatterns = [
    path('api/sales/', SalesReportView.as_view(), name='sales-report'),
    path('api/inventory/', InventoryReportView.as_view(), name='inventory-report'),
    path('api/products/', ProductReportView.as_view(), name='product-report'),
    path('api/export/', ExportDataView.as_view(), name='export-data'),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
]

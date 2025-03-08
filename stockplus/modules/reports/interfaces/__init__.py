"""
Reports interfaces.
This module contains the interfaces for the reports module.
"""

from stockplus.modules.reports.interfaces.views import (
    SalesReportView,
    InventoryReportView,
    ProductReportView,
    ExportDataView,
    DashboardView,
)
from stockplus.modules.reports.interfaces.serializers import (
    SalesReportSerializer,
    InventoryReportSerializer,
    ProductReportSerializer,
    ExportDataSerializer,
    DashboardDataSerializer,
)
from stockplus.modules.reports.interfaces.urls import urlpatterns

__all__ = [
    'SalesReportView',
    'InventoryReportView',
    'ProductReportView',
    'ExportDataView',
    'DashboardView',
    'SalesReportSerializer',
    'InventoryReportSerializer',
    'ProductReportSerializer',
    'ExportDataSerializer',
    'DashboardDataSerializer',
    'urlpatterns',
]

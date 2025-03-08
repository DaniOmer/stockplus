from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stockplus.modules.sales.interfaces.views import SaleViewSet, InvoiceViewSet

router = DefaultRouter()
router.register(r'api/sales', SaleViewSet, basename='sale')
router.register(r'api/invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('', include(router.urls)),
]

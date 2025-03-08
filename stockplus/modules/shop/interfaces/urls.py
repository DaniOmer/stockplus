"""
URL configuration for the shop application.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stockplus.modules.shop.interfaces.views import (
    ProductViewSet,
    PriceViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'prices', PriceViewSet, basename='price')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

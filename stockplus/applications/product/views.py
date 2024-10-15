from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from builder.models import Company

from stockplus.models import Brand, ProductCategory, Product, ProductFeature
from stockplus.applications.product.serializers import (
    BrandSerializer, ProductSerializer, 
    ProductCategorySerializer, ProductFeatureSerializer,
    ProductVariantSerializer, PointOfSaleProductVariantSerializer
)

class BrandViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the brands
    associated with the user company.
    """
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        company = self.request.user.company
        if not company:
            raise NotFound({"detail": "You must create a company to continue."})

        return Brand.objects.filter(company=company)

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the product categories
    associated with the user company.
    """
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        company = self.request.user.company
        if not company:
            raise NotFound({"detail": "You must create a company to continue."})

        return ProductCategory.objects.filter(company=company)

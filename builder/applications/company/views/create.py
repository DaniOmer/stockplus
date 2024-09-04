from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from builder.permissions import base_permissions
from builder.models import Company, CompanyAddress
from builder.applications.company.serializers import CompanySerializer, CompanyAddressSerializer


class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = base_permissions

    def perform_create(self, serializer):

        if Company.objects.filter(owner=self.request.user).exists():
            raise serializers.ValidationError({"detail": "There's already one company associated to this company."})
        serializer.save(owner=self.request.user)


class CompanyAddressCreateView(generics.CreateAPIView):
    """
    API endpoint to create Company Address
    """
    serializer_class = CompanyAddressSerializer
    permission_classes = base_permissions

    def perform_create(self, serializer):
        try:
            company = Company.objects.get(owner=self.request.user)
        except Company.DoesNotExist:
            raise serializers.ValidationError({"detail": "You must create a company before creating an associated address."})
        
        if CompanyAddress.objects.filter(company=company).exists():
            raise serializers.ValidationError({"detail": "There's already one address associated to this company."})
        
        serializer.save(company=company)
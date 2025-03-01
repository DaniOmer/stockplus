from rest_framework import generics, serializers

from builder.permissions import base_permissions
from builder.models import Company, CompanyAddress
from builder.modules.company.serializers import CompanySerializer, CompanyAddressSerializer


class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = base_permissions

    def perform_create(self, serializer):
        if self.request.user.company is not None:
            raise serializers.ValidationError({"detail": "There's already one company associated to this user."})
        serializer.save()
        company = serializer.instance
        self.request.user.company = company
        self.request.user.save()

class CompanyAddressCreateView(generics.CreateAPIView):
    """
    API endpoint to create Company Address
    """
    serializer_class = CompanyAddressSerializer
    permission_classes = base_permissions

    def perform_create(self, serializer):
        company = self.request.user.company
        if company is not None:
            raise serializers.ValidationError({"detail": "You must create a company before creating an associated address."})
        
        if CompanyAddress.objects.filter(company=company).exists():
            raise serializers.ValidationError({"detail": "There's already one address associated to this company."})
        
        serializer.save(company=company)
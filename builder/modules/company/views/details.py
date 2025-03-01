from rest_framework import generics

from builder.permissions import base_permissions
from builder.models import Company, CompanyAddress
from builder.modules.user.permissions import IsSelf
from builder.modules.company.serializers import CompanySerializer, CompanyAddressSerializer

class CompanyDetailsView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to get or update company details
    """
    serializer_class = CompanySerializer
    permission_classes = base_permissions

    def get_queryset(self):
        company_id = self.kwargs.get('pk')
        return Company.objects.filter(id=company_id)
    

class CompanyAddressDetailsView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to get or update Company Address
    """
    queryset = CompanyAddress.objects.all()
    serializer_class = CompanyAddressSerializer
    permission_classes = base_permissions

    def get_queryset(self):
        address_id = self.kwargs.get('pk')
        return self.queryset.filter(id=address_id)
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from builder.models import Company, CompanyAddress
from builder.applications.user.permissions import IsSelf
from builder.applications.company.serializers import CompanySerializer, CompanyAddressSerializer

CrudPersmission = getattr(settings, 'CRUD_PERMISSION', None)

class CompanyDetailsView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to get or update company details
    """
    serializer_class = CompanySerializer
    permission_classes = [CrudPersmission & IsAuthenticated & IsSelf] if CrudPersmission else [IsAuthenticated & IsSelf]

    def get_queryset(self):
        company_id = self.kwargs.get('pk')
        return Company.objects.filter(id=company_id)
    

class CompanyAddressDetailsView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to get or update Company Address
    """
    queryset = CompanyAddress.objects.all()
    serializer_class = CompanyAddressSerializer
    permission_classes = [CrudPersmission & IsAuthenticated & IsSelf] if CrudPersmission else [IsAuthenticated & IsSelf]

    def get_queryset(self):
        address_id = self.kwargs.get('pk')
        return self.queryset.filter(id=address_id)
from rest_framework import generics

from builder.permissions import base_permissions
from builder.models import Company
from builder.modules.company.interfaces.serializers import CompanySerializer

class CompanyDetailsView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to get or update company details
    """
    serializer_class = CompanySerializer
    permission_classes = base_permissions

    def get_queryset(self):
        company_id = self.kwargs.get('pk')
        return Company.objects.filter(id=company_id)
    
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from builder.applications.company.serializers import CompanySerializer

CreateCompanyPersmission = getattr(settings, 'CREATE_COMPANY_PERMISSION', None)

class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = CreateCompanyPersmission if CreateCompanyPersmission else [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

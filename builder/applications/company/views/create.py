from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from builder.applications.company.serializers import CompanySerializer

CompanyCrudPersmission = getattr(settings, 'COMPANY_CRUD_PERMISSION', None)

class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = CompanyCrudPersmission if CompanyCrudPersmission else [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

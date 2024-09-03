from django.conf import settings
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from builder.models import Company
from builder.applications.company.serializers import CompanySerializer

CompanyCrudPersmission = getattr(settings, 'COMPANY_CRUD_PERMISSION', None)

class CompanyDetailsView(generics.RetrieveUpdateAPIView):
    serializer_class = CompanySerializer
    permission_classes = CompanyCrudPersmission if CompanyCrudPersmission else [IsAuthenticated]

    def get_queryset(self):
        """
        Restricts the returned company details by filtering against the 'id' query parameter 
        and ensuring the requesting user is the owner of the company.
        """
        company_id = self.kwargs.get('pk')
        user = self.request.user
        return Company.objects.filter(id=company_id, owner=user)
    
    def update(self, request, *args, **kwargs):
        company = self.get_object()
        if request.user != company.owner:
            # return Response(
            #     {"detail": "You do not have permission to update this company."}, 
            #     status=status.HTTP_401_UNAUTHORIZED
            # )
            raise PermissionDenied("You do not have permission to update this company.")
        return super().update(request, *args, **kwargs)
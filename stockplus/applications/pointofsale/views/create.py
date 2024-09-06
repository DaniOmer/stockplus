from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from builder.models import Company
from stockplus.models import PointOfSale
from stockplus.applications.pointofsale.permissions import RoleBasedAccess
from stockplus.applications.pointofsale.serializers import PointOfSaleSerializer


class PointOfSaleListCreateView(generics.ListCreateAPIView):
    queryset = PointOfSale.objects.all()
    serializer_class = PointOfSaleSerializer
    permission_classes = [RoleBasedAccess]
    allowed_groups = ["Manager"]

    def get_queryset(self):
        user = self.request.user
        try:
            company = Company.objects.get(owner=user)
            return PointOfSale.objects.filter(company=company)
        except Company.DoesNotExist:
            return PointOfSale.objects.none()
        
    def perform_create(self, serializer):
        user = self.request.user
        try:
            company = Company.objects.get(owner=user)
        except Company.DoesNotExist:
            raise ValidationError("You must create a company to continue.")
        serializer.save(company=company)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response(
                {"detail": "Please provide your company informations to continue."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PointOfSaleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


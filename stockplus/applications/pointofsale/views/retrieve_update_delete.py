from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied

from builder.models import Company
from stockplus.models import PointOfSale
from stockplus.applications.pointofsale.serializers import PointOfSaleSerializer


class PointOfSaleRetrievUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PointOfSale.objects.all()
    serializer_class = PointOfSaleSerializer

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        try:
            company = Company.objects.get(owner=user)
        except Company.DoesNotExist:
            raise ValidationError("You must create a company to continue.")
        
        if obj.company != company and not user in obj.collaborators.all():
            raise PermissionDenied("You do not have permission to access this resource.")
        return obj
    
    def perform_update(self, serializer):
        user = self.request.user
        user_groups = user.groups.values_list('name', flat=True)
        if "Manager" not in user_groups:
            raise PermissionDenied("You do not have permission to update this resource.")
        serializer.save()
    
    def perform_destroy(self, instance):
        user = self.request.user
        user_groups = user.groups.values_list('name', flat=True)
        if "Manager" not in user_groups:
            raise PermissionDenied("You do not have permission to delete this resource.")
        instance.delete()
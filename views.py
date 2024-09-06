from django.shortcuts import get_object_or_404
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response

from builder.permissions import base_permissions

from stockplus.models import PointOfSale
from stockplus.applications.pointofsale.serializers import PointOfSaleSerializer

class PointOfSaleViewSet(viewsets.ViewSet):
    """
    A viewsets for CRUD operations on a point of sale
    """
    permission_classes = base_permissions

    def list(self, request):
        permission_classes = [base_permissions]

        queryset = PointOfSale.objects.all()
        serializer = PointOfSaleSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PointOfSaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Something went wrong while creating a new PointOfSale.", "errors": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, permission_classes=[])
    def retrieve(self, request, pk=None):
        queryset = PointOfSale.objects.all()
        point_of_sale = get_object_or_404(queryset, pk=pk)
        user = self.request.user

        if user in point_of_sale.collaborators.all() or user == point_of_sale.company.owner:
            serializer = self.get_serializer(point_of_sale)
            return Response(serializer.data)
        return Response({"detail": "You do not have permission to view this PointOfSale."}, status=status.HTTP_403_FORBIDDEN)

    # @permission_classes([base_permissions])
    def update(self, request, pk=None):
        queryset = PointOfSale.objects.all()
        point_of_sale = get_object_or_404(queryset, pk=pk)
        serializer = PointOfSaleSerializer(data=point_of_sale)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(
            {"detail": "Something went wrong while updating the PointOfSale.", "errors": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # @permission_classes([base_permissions])
    def partial_update(self, request, pk=None):
        pass
    
    # @permission_classes([base_permissions])
    def destroy(self, request, pk=None):
        pass
from rest_framework import viewsets
from rest_framework.response import Response

from stockplus.applications.pointofsale.serializers import PointOfSaleSerializer

class PointOfSaleViewSet(viewsets.ViewSet):
    """
    A viewsets for CRUD operations on a point of sale
    """

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
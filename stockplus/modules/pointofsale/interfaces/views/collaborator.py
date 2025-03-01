from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from stockplus.modules.pointofsale.application.services import PointOfSaleService
from stockplus.modules.pointofsale.domain.exceptions import (
    PointOfSaleNotFoundError, CollaboratorNotFoundError
)
from stockplus.modules.pointofsale.infrastructure.orm.orm import PointOfSaleORM
from stockplus.modules.pointofsale.interfaces.serializers import PointOfSaleAddCollaboratorSerializer


class PointOfSaleAddCollaboratorView(generics.GenericAPIView):
    """
    API view for adding a collaborator to a point of sale.
    """
    queryset = PointOfSaleORM.objects.all()
    serializer_class = PointOfSaleAddCollaboratorSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.point_of_sale_service = None
    
    def get_point_of_sale_service(self) -> PointOfSaleService:
        """
        Get the point of sale service from the dependency container.
        
        Returns:
            The point of sale service.
        """
        if not self.point_of_sale_service:
            from stockplus.config.dependencies import get_point_of_sale_service
            self.point_of_sale_service = get_point_of_sale_service()
        return self.point_of_sale_service
    
    def get_queryset(self):
        """
        Get the queryset for the view.
        
        Returns:
            The queryset.
        """
        company = self.request.user.company
        return PointOfSaleORM.objects.filter(company=company)
    
    def get_object(self):
        """
        Get the point of sale object.
        
        Returns:
            The point of sale object.
            
        Raises:
            NotFound: If the point of sale is not found.
        """
        try:
            return super().get_object()
        except NotFound:
            raise NotFound("Point of sale not found.")
    
    def post(self, request, *args, **kwargs):
        """
        Add a collaborator to a point of sale.
        
        Returns:
            Response with the result of the operation.
        """
        point_of_sale = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        collaborator_id = serializer.get_collaborator_id()
        
        service = self.get_point_of_sale_service()
        try:
            service.add_collaborator(point_of_sale.id, collaborator_id)
            return Response(
                {"detail": "Collaborator added successfully."},
                status=status.HTTP_200_OK
            )
        except PointOfSaleNotFoundError:
            raise NotFound("Point of sale not found.")
        except CollaboratorNotFoundError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

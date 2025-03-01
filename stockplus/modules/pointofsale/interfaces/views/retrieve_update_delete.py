from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from stockplus.modules.pointofsale.application.services import PointOfSaleService
from stockplus.modules.pointofsale.domain.exceptions import PointOfSaleNotFoundError
from stockplus.modules.pointofsale.infrastructure.orm.orm import PointOfSaleORM
from stockplus.modules.pointofsale.interfaces.serializers import PointOfSaleSerializer


class PointOfSaleRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a point of sale.
    """
    queryset = PointOfSaleORM.objects.all()
    serializer_class = PointOfSaleSerializer
    
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
    
    def perform_update(self, serializer):
        """
        Update a point of sale.
        
        Args:
            serializer: The serializer with the validated data.
        """
        point_of_sale = serializer.to_domain()
        point_of_sale.id = self.get_object().id
        
        service = self.get_point_of_sale_service()
        try:
            service.update_point_of_sale(
                point_of_sale_id=point_of_sale.id,
                name=point_of_sale.name,
                type=point_of_sale.type,
                opening_hours=point_of_sale.opening_hours,
                closing_hours=point_of_sale.closing_hours
            )
            
            # Update collaborators if any
            existing_point_of_sale = service.get_point_of_sale(point_of_sale.id)
            
            # Remove collaborators that are not in the new list
            for collaborator_id in existing_point_of_sale.collaborator_ids:
                if collaborator_id not in point_of_sale.collaborator_ids:
                    service.remove_collaborator(point_of_sale.id, collaborator_id)
            
            # Add collaborators that are not in the existing list
            for collaborator_id in point_of_sale.collaborator_ids:
                if collaborator_id not in existing_point_of_sale.collaborator_ids:
                    service.add_collaborator(point_of_sale.id, collaborator_id)
                    
        except PointOfSaleNotFoundError:
            raise NotFound("Point of sale not found.")
    
    def perform_destroy(self, instance):
        """
        Delete a point of sale.
        
        Args:
            instance: The point of sale to delete.
        """
        service = self.get_point_of_sale_service()
        try:
            service.delete_point_of_sale(instance.id)
        except PointOfSaleNotFoundError:
            raise NotFound("Point of sale not found.")

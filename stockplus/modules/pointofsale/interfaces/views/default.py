from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from stockplus.modules.pointofsale.application.services import PointOfSaleService
from stockplus.modules.pointofsale.domain.exceptions import PointOfSaleNotFoundError


class SetDefaultPointOfSaleView(APIView):
    """
    API view for setting a point of sale as the default.
    """
    
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
    
    def post(self, request, pk, *args, **kwargs):
        """
        Set a point of sale as the default.
        
        Args:
            request: The request object.
            pk: The ID of the point of sale to set as default.
            
        Returns:
            Response with the updated point of sale.
            
        Raises:
            NotFound: If the point of sale is not found.
        """
        service = self.get_point_of_sale_service()
        
        try:
            # Check if the point of sale belongs to the user's company
            point_of_sale = service.get_point_of_sale(pk)
            if point_of_sale.company_id != request.user.company.id:
                raise ValidationError("Point of sale not found.")
            
            # Set the point of sale as default
            updated_point_of_sale = service.set_default_point_of_sale(pk)
            
            return Response(
                {"detail": f"Point of sale '{updated_point_of_sale.name}' set as default."},
                status=status.HTTP_200_OK
            )
        except PointOfSaleNotFoundError:
            raise NotFound("Point of sale not found.")

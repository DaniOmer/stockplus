from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from stockplus.modules.company.infrastructure.models.company_model import Company
from stockplus.modules.pointofsale.infrastructure.models.pos_model import PointOfSale
from stockplus.modules.pointofsale.application.services import PointOfSaleService
from stockplus.modules.pointofsale.domain.exceptions import PointOfSaleLimitExceededError
from stockplus.modules.pointofsale.interfaces.serializers import PointOfSaleSerializer


class PointOfSaleListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating points of sale.
    """
    queryset = PointOfSale.objects.all()
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
            
        Raises:
            ValidationError: If the user does not have a company.
        """
        company = self.request.user.company
        if not company:
            raise ValidationError("You must create a company to continue.")
        
        try:
            return PointOfSale.objects.filter(company=company)
        except Company.DoesNotExist:
            return PointOfSale.objects.none()
        
    def perform_create(self, serializer):
        """
        Create a new point of sale.
        
        Args:
            serializer: The serializer with the validated data.
            
        Raises:
            ValidationError: If the user does not have a company.
            ValidationError: If the company has exceeded its point of sale limit.
        """
        company = self.request.user.company
        if not company:
            raise ValidationError("You must create a company to continue.")
        
        # Convert serializer data to domain model
        point_of_sale = serializer.to_domain()
        point_of_sale.company_id = company.id
        
        # Create the point of sale using the service
        service = self.get_point_of_sale_service()
        
        try:
            created_point_of_sale = service.create_point_of_sale(
                name=point_of_sale.name,
                company_id=point_of_sale.company_id,
                type=point_of_sale.type,
                opening_hours=point_of_sale.opening_hours,
                closing_hours=point_of_sale.closing_hours,
                is_default=point_of_sale.is_default
            )
            
            # Add collaborators if any
            for collaborator_id in point_of_sale.collaborator_ids:
                service.add_collaborator(created_point_of_sale.id, collaborator_id)
                
        except PointOfSaleLimitExceededError as e:
            raise ValidationError(str(e))
        
    def list(self, request, *args, **kwargs):
        """
        List all points of sale for the user's company.
        
        Returns:
            Response with the list of points of sale.
        """
        queryset = self.get_queryset()
        if not queryset:
            return Response(
                {"message": "Please provide your company information to continue."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PointOfSaleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

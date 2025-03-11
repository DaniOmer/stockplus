from rest_framework import viewsets, status
from rest_framework.response import Response

from stockplus.modules.product.application.services import BrandService
from stockplus.modules.product.infrastructure.repositories import BrandRepository
from stockplus.modules.product.domain.exceptions import BrandNotFoundError
from stockplus.modules.product.infrastructure.models.brand_model import Brand as BrandORM
from stockplus.modules.product.interfaces.serializers import BrandSerializer
from stockplus.modules.company.infrastructure.repositories import CompanyRepository

class BrandViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing brands.
    """
    queryset = BrandORM.objects.all()
    serializer_class = BrandSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        brand_repository = BrandRepository()
        company_repository = CompanyRepository()
        self.brand_service = BrandService(brand_repository, company_repository)
    
    def get_queryset(self):
        """
        Get the queryset for the view.
        
        Returns:
            The queryset.
        """
        company = self.request.user.company_id
        return BrandORM.objects.filter(company=company)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new brand.
        
        Returns:
            Response with the created brand.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the company ID from the request user
        company_id = request.user.company_id
        if not company_id:
            return Response(
                {
                    "message": "You must create a company first."
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert serializer data to domain model
        brand = serializer.to_domain()
        
        # Create the brand using the service
        try:
            created_brand = self.brand_service.create_brand(
                name=brand.name,
                company_id=company_id,
                description=brand.description,
                logo_url=brand.logo_url
            )
            
            return Response(
                {
                    "message": "Brand created successfully.", 
                    "data": {
                        "id": created_brand.id,
                        "name": created_brand.name,
                        "description": created_brand.description,
                        "logo_url": created_brand.logo_url
                    }
                },
                status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Update an existing brand.
        
        Returns:
            Response with the updated brand.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Convert serializer data to domain model
        brand = serializer.to_domain()
        brand.id = instance.id
        
        try:
            updated_brand = self.brand_service.update_brand(
                brand_id=brand.id,
                name=brand.name,
                description=brand.description,
                logo_url=brand.logo_url
            )
            
            return Response(
                {
                    "message": "Brand updated successfully.",
                    "data": {
                        "id": updated_brand.id,
                        "name": updated_brand.name,
                        "description": updated_brand.description,
                        "logo_url": updated_brand.logo_url
                    }
                },
                status=status.HTTP_200_OK
            )
        except BrandNotFoundError:
            return Response(
                {
                    "message": "Brand not found."
                }, 
                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a brand.
        
        Returns:
            Response with no content.
        """
        instance = self.get_object()
        
        try:
            self.brand_service.delete_brand(instance.id)
            return Response(
                {
                    "message": "Brand deleted successfully."
                },
                status=status.HTTP_204_NO_CONTENT)
        except BrandNotFoundError:
            return Response({"message": "Brand not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

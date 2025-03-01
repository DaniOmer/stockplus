from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from stockplus.modules.product.application.services import BrandService
from stockplus.modules.product.domain.exceptions import BrandNotFoundError
from stockplus.modules.product.infrastructure.orm import Brand as BrandORM
from stockplus.modules.product.interfaces.serializers import BrandSerializer


class BrandViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing brands.
    """
    queryset = BrandORM.objects.all()
    serializer_class = BrandSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.brand_service = None
    
    def get_brand_service(self) -> BrandService:
        """
        Get the brand service from the dependency container.
        
        Returns:
            The brand service.
        """
        if not self.brand_service:
            from stockplus.config.dependencies import get_brand_service
            self.brand_service = get_brand_service()
        return self.brand_service
    
    def get_queryset(self):
        """
        Get the queryset for the view.
        
        Returns:
            The queryset.
        """
        company = self.request.user.company
        if not company:
            return BrandORM.objects.none()
        
        return BrandORM.objects.filter(company=company)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new brand.
        
        Returns:
            Response with the created brand.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Convert serializer data to domain model
        brand = serializer.to_domain()
        brand.company_id = request.user.company.id
        
        # Create the brand using the service
        service = self.get_brand_service()
        try:
            created_brand = service.create_brand(
                name=brand.name,
                company_id=brand.company_id,
                description=brand.description,
                logo_url=brand.logo_url
            )
            
            # Get the ORM brand to return
            orm_brand = BrandORM.objects.get(id=created_brand.id)
            result_serializer = self.get_serializer(orm_brand)
            
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
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
        
        # Update the brand using the service
        service = self.get_brand_service()
        try:
            updated_brand = service.update_brand(
                brand_id=brand.id,
                name=brand.name,
                description=brand.description,
                logo_url=brand.logo_url
            )
            
            # Get the ORM brand to return
            orm_brand = BrandORM.objects.get(id=updated_brand.id)
            result_serializer = self.get_serializer(orm_brand)
            
            return Response(result_serializer.data)
        except BrandNotFoundError:
            return Response({"detail": "Brand not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a brand.
        
        Returns:
            Response with no content.
        """
        instance = self.get_object()
        
        # Delete the brand using the service
        service = self.get_brand_service()
        try:
            service.delete_brand(instance.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BrandNotFoundError:
            return Response({"detail": "Brand not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

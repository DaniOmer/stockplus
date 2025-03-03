from rest_framework import viewsets, status
from rest_framework.response import Response

from stockplus.modules.product.application.services import ProductCategoryService
from stockplus.modules.product.domain.exceptions import ProductCategoryNotFoundError
from stockplus.infrastructure.models import ProductCategory as ProductCategoryORM
from stockplus.modules.product.interfaces.serializers import ProductCategorySerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing product categories.
    """
    queryset = ProductCategoryORM.objects.all()
    serializer_class = ProductCategorySerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category_service = None
    
    def get_category_service(self) -> ProductCategoryService:
        """
        Get the product category service from the dependency container.
        
        Returns:
            The product category service.
        """
        if not self.category_service:
            from stockplus.config.dependencies import get_product_category_service
            self.category_service = get_product_category_service()
        return self.category_service
    
    def get_queryset(self):
        """
        Get the queryset for the view.
        
        Returns:
            The queryset.
        """
        company = self.request.user.company
        if not company:
            return ProductCategoryORM.objects.none()
        
        return ProductCategoryORM.objects.filter(company=company)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new product category.
        
        Returns:
            Response with the created product category.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Convert serializer data to domain model
        category = serializer.to_domain()
        category.company_id = request.user.company.id
        
        # Create the product category using the service
        service = self.get_category_service()
        try:
            created_category = service.create_category(
                name=category.name,
                company_id=category.company_id,
                description=category.description,
                parent_id=category.parent_id
            )
            
            # Get the ORM product category to return
            orm_category = ProductCategoryORM.objects.get(id=created_category.id)
            result_serializer = self.get_serializer(orm_category)
            
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Update an existing product category.
        
        Returns:
            Response with the updated product category.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Convert serializer data to domain model
        category = serializer.to_domain()
        category.id = instance.id
        
        # Update the product category using the service
        service = self.get_category_service()
        try:
            updated_category = service.update_category(
                category_id=category.id,
                name=category.name,
                description=category.description,
                parent_id=category.parent_id
            )
            
            # Get the ORM product category to return
            orm_category = ProductCategoryORM.objects.get(id=updated_category.id)
            result_serializer = self.get_serializer(orm_category)
            
            return Response(result_serializer.data)
        except ProductCategoryNotFoundError:
            return Response({"detail": "Product category not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a product category.
        
        Returns:
            Response with no content.
        """
        instance = self.get_object()
        
        # Delete the product category using the service
        service = self.get_category_service()
        try:
            service.delete_category(instance.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductCategoryNotFoundError:
            return Response({"detail": "Product category not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

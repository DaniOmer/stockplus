from rest_framework import viewsets, status
from rest_framework.response import Response

from stockplus.modules.product.application.services import ProductService
from stockplus.modules.product.domain.exceptions import ProductNotFoundError
from stockplus.modules.product.infrastructure.models import Product as ProductORM
from stockplus.modules.product.interfaces.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API viewset for managing products.
    """
    queryset = ProductORM.objects.all()
    serializer_class = ProductSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = None
    
    def get_product_service(self) -> ProductService:
        """
        Get the product service from the dependency container.
        
        Returns:
            The product service.
        """
        if not self.product_service:
            from stockplus.config.dependencies import get_product_service
            self.product_service = get_product_service()
        return self.product_service
    
    def get_queryset(self):
        """
        Get the queryset for the view.
        
        Returns:
            The queryset.
        """
        company = self.request.user.company
        if not company:
            return ProductORM.objects.none()
        
        return ProductORM.objects.filter(company=company)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new product.
        
        Returns:
            Response with the created product.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Convert serializer data to domain model
        product = serializer.to_domain()
        product.company_id = request.user.company.id
        
        # Create the product using the service
        service = self.get_product_service()
        try:
            created_product = service.create_product(
                name=product.name,
                company_id=product.company_id,
                description=product.description,
                brand_id=product.brand_id,
                category_id=product.category_id
            )
            
            # Add features if any
            for feature in product.features:
                service.add_feature(
                    product_id=created_product.id,
                    name=feature.name,
                    description=feature.description
                )
            
            # Add variants if any
            for variant in product.variants:
                service.add_variant(
                    product_id=created_product.id,
                    name=variant.name,
                    color=variant.color,
                    size=variant.size,
                    price=variant.price,
                    buy_price=variant.buy_price,
                    sku=variant.sku
                )
            
            # Get the ORM product to return
            orm_product = ProductORM.objects.get(id=created_product.id)
            result_serializer = self.get_serializer(orm_product)
            
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        Update an existing product.
        
        Returns:
            Response with the updated product.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Convert serializer data to domain model
        product = serializer.to_domain()
        product.id = instance.id
        
        # Update the product using the service
        service = self.get_product_service()
        try:
            updated_product = service.update_product(
                product_id=product.id,
                name=product.name,
                description=product.description,
                brand_id=product.brand_id,
                category_id=product.category_id
            )
            
            # Update features if any
            if product.features:
                # Delete existing features
                for feature in instance.features.all():
                    service.delete_feature(feature.id)
                
                # Add new features
                for feature in product.features:
                    service.add_feature(
                        product_id=updated_product.id,
                        name=feature.name,
                        description=feature.description
                    )
            
            # Update variants if any
            if product.variants:
                # Delete existing variants
                for variant in instance.variants.all():
                    service.delete_variant(variant.id)
                
                # Add new variants
                for variant in product.variants:
                    service.add_variant(
                        product_id=updated_product.id,
                        name=variant.name,
                        color=variant.color,
                        size=variant.size,
                        price=variant.price,
                        buy_price=variant.buy_price,
                        sku=variant.sku
                    )
            
            # Get the ORM product to return
            orm_product = ProductORM.objects.get(id=updated_product.id)
            result_serializer = self.get_serializer(orm_product)
            
            return Response(result_serializer.data)
        except ProductNotFoundError:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a product.
        
        Returns:
            Response with no content.
        """
        instance = self.get_object()
        
        # Delete the product using the service
        service = self.get_product_service()
        try:
            service.delete_product(instance.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductNotFoundError:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

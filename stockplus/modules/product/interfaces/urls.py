from rest_framework import routers

from stockplus.modules.product.interfaces.views import (
    BrandViewSet, ProductCategoryViewSet, ProductViewSet
)

router = routers.SimpleRouter()
router.register(r'api/brands', BrandViewSet, basename="brands")
router.register(r'api/categories', ProductCategoryViewSet, basename="categories")
router.register(r'api/products', ProductViewSet, basename="products")

urlpatterns = router.urls

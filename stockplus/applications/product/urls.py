from rest_framework import routers

from stockplus.applications.product import views

router = routers.SimpleRouter()
router.register(r'api/brand', views.BrandViewSet, basename="brands")
router.register(r'api/category', views.ProductCategoryViewSet, basename="categories")
# router.register(r'api/products', views.ProductViewSet, basename="products")

urlpatterns = router.urls
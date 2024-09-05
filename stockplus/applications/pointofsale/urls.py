from stockplus.applications.pointofsale.views import PointOfSaleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/pointofsale', PointOfSaleViewSet, basename='pointofsale')
urlpatterns = router.urls
from stockplus.applications.pointofsale.views import PointOfSaleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', PointOfSaleViewSet, basename='user')
urlpatterns = router.urls
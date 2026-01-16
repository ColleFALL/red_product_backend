from rest_framework.routers import DefaultRouter
from .views import HotelViewSet

router = DefaultRouter()
router.register(r"", HotelViewSet, basename="hotels")

urlpatterns = router.urls

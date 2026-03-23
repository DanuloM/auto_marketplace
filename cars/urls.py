from .views import ManufacturerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
urlpatterns = router.urls

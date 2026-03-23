from .views import ManufacturerViewSet, ModelViewSet, GenerationViewSet, CarViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'models', ModelViewSet, basename='model')
router.register(r'generations', GenerationViewSet, basename='generation')
router.register(r'cars', CarViewSet, basename='car')
urlpatterns = router.urls

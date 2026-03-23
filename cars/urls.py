from .views import ManufacturerViewSet, ModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'models', ModelViewSet, basename='model')
urlpatterns = router.urls

from .serializers import (
    ManufacturerSerializer,
    ModelSerializer,
    GenerationSerializer,
    CarSerializer,
)
from .models import Manufacturer, Model, Generation, Car, PriceHistory
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.permissions import IsAdmin


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdmin()]


class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdmin()]


class GenerationViewSet(viewsets.ModelViewSet):
    queryset = Generation.objects.all()
    serializer_class = GenerationSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdmin()]


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        if self.action in ["destroy", "update", "partial_update", "create"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == "admin":
            return Car.objects.all()
        if not self.request.user.is_authenticated:
            return Car.objects.filter(is_active=True)
        if self.action in ["destroy", "update", "partial_update"]:
            return Car.objects.filter(seller=self.request.user)
        return Car.objects.filter(is_active=True)

    def perform_create(self, serializer) -> None:
        car = serializer.save(seller=self.request.user)
        PriceHistory.objects.create(car=car, price=car.price)

    def perform_update(self, serializer) -> None:
        old_price = serializer.instance.price
        updated_car = serializer.save()
        if old_price != updated_car.price:
            PriceHistory.objects.create(
                car=updated_car,
                price=updated_car.price,
            )
        
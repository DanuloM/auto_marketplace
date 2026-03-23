from .serializers import ManufacturerSerializer, ModelSerializer, GenerationSerializer
from .models import Manufacturer, Model, Generation
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
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

from rest_framework import serializers

from .models import Manufacturer, Model, Generation

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name']




class ModelSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(read_only=True)
    manufacturer_id = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all(),
        source='manufacturer',
        write_only=True
    )
    
    class Meta:
        model = Model
        fields = ['id', 'name', 'manufacturer', 'manufacturer_id']


class GenerationSerializer(serializers.ModelSerializer):
    model = ModelSerializer(read_only=True)
    model_id = serializers.PrimaryKeyRelatedField(
        queryset=Model.objects.all(),
        source='model',
        write_only=True
    )
    
    class Meta:
        model = Generation
        fields = ['id', 'name', 'year_start', 'year_end', 'model', 'model_id']

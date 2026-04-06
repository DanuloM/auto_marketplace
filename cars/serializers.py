from rest_framework import serializers

from .models import Manufacturer, Model, Generation, Car, PriceHistory, CarImage

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


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['price', 'created_at']


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image']

    def validate(self, attrs):
        car = attrs.get('car')
        if CarImage.objects.filter(car=car).count() >= 10:
            raise serializers.ValidationError("Limit 10 images per car")
        return attrs


class CarSerializer(serializers.ModelSerializer):
    generation = serializers.CharField(read_only=True, source='generation.name')
    generation_id = serializers.PrimaryKeyRelatedField(
        queryset=Generation.objects.all(),
        source='generation',
        write_only=True
    )
    model = serializers.CharField(read_only=True, source='model.name')
    model_id = serializers.PrimaryKeyRelatedField(
        queryset=Model.objects.all(),
        source='model',
        write_only=True
    )
    price_history = PriceHistorySerializer(many=True, read_only=True)
    images = CarImageSerializer(many=True, read_only=True)
    class Meta:
        model = Car
        fields = ['id', 'model', 'model_id', 'generation', 'generation_id', 'body_type', 'color', 'vin', 'owner_count', 'seller', 'price', 'price_history','mileage', 'year', 'description', 'images', 'is_active', 'created_at']
        read_only_fields = ['id', 'seller', 'created_at']


    def validate_year(self, value):
        if value < 1886 or value > 2026:
            raise serializers.ValidationError("Year must be between 1886 and 2026")
        return value

    def validate(self, data):
        generation = data.get('generation')
        model = data.get('model')
        year = data.get('year')

        if model and generation and model != generation.model:
            raise serializers.ValidationError("Generation does not belong to the selected model.")

        if year and generation:
            if generation.year_start and year < generation.year_start:
                raise serializers.ValidationError("Year is before generation start year.")
            if generation.year_end and year > generation.year_end:
                raise serializers.ValidationError("Year is after generation end year.")

        return super().validate(data)

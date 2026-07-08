import django_filters
from .models import Car


class CarFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name="model__manufacturer__name")

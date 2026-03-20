from django.db import models

from django.conf import settings
# Create your models here.



class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Model(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.manufacturer.name} {self.name}"
    
    class Meta:
        unique_together = ('name', 'manufacturer')


class Generation(models.Model):
    name = models.CharField(max_length=100)
    year_start = models.PositiveSmallIntegerField(null=True, blank=True)
    year_end = models.PositiveSmallIntegerField(null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.model.manufacturer.name} {self.model.name} {self.name}"
    
    class Meta:
        unique_together = ('name', 'model')


class BodyType(models.TextChoices):
    SEDAN = 'Sedan'
    HATCHBACK = 'Hatchback'
    SUV = 'SUV'
    COUPE = 'Coupe'
    CONVERTIBLE = 'Convertible'
    WAGON = 'Wagon'
    VAN = 'Van'


class Car(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    generation = models.ForeignKey(Generation, on_delete=models.CASCADE)
    body_type = models.CharField(max_length=20, choices=BodyType.choices)
    color = models.CharField(max_length=50, null=True, blank=True)
    vin = models.CharField(max_length=17, unique=True, null=True, blank=True)
    owner_count = models.PositiveIntegerField(default=0)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField()
    year = models.PositiveSmallIntegerField()
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.generation} - {self.body_type}"

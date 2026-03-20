from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserRole(models.TextChoices):
    USER = 'user', 'User'
    ADMIN = 'admin', 'Admin'


class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.USER)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

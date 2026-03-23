from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Manufacturer, Model, Generation, Car

User = get_user_model()


class CarsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="AdminPass123!",
            role="admin",
        )
        self.user = User.objects.create_user(
            username="user", email="user@example.com", password="UserPass123!"
        )
        self.admin_token = RefreshToken.for_user(self.admin).access_token
        self.user_token = RefreshToken.for_user(self.user).access_token

        # Catalog data
        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.model = Model.objects.create(
            name="Corolla", manufacturer=self.manufacturer
        )
        self.generation = Generation.objects.create(
            name="E120", year_start=2000, year_end=2006, model=self.model
        )

        self.car_data = {
            "model_id": self.model.id,
            "generation_id": self.generation.id,
            "body_type": "Sedan",
            "color": "Black",
            "vin": "1HGBH41JXMN109186",
            "owner_count": 1,
            "price": "15000.00",
            "mileage": 120000,
            "year": 2004,
            "description": "Good condition",
        }

    def test_manufacturer_list_anon(self):
        response = self.client.get("/api/manufacturers/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_manufacturer_list_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get("/api/manufacturers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_manufacturer_create_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.post(
            "/api/manufacturers/", {"name": "Honda"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Manufacturer.objects.filter(name="Honda").exists())

    def test_manufacturer_create_user_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.post(
            "/api/manufacturers/", {"name": "Ford"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_car_create_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.post("/api/cars/", self.car_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        car = Car.objects.get(id=response.data["id"])
        self.assertEqual(car.seller, self.user)

    def test_car_create_anon_forbidden(self):
        response = self.client.post("/api/cars/", self.car_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_car_update_owner(self):
        car = Car.objects.create(
            model=self.model,
            generation=self.generation,
            body_type="Sedan",
            vin="1HGBH41JXMN109186",
            owner_count=1,
            price="15000.00",
            mileage=120000,
            year=2004,
            seller=self.user,
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        payload = {"price": "14000.00"}
        response = self.client.patch(f"/api/cars/{car.id}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car.refresh_from_db()
        self.assertEqual(str(car.price), "14000.00")

    def test_car_update_non_owner_forbidden(self):
        other = User.objects.create_user(
            username="other", email="other@example.com", password="OtherPass123!"
        )
        car = Car.objects.create(
            model=self.model,
            generation=self.generation,
            body_type="Sedan",
            vin="1HGBH41JXMN109186",
            owner_count=1,
            price="15000.00",
            mileage=120000,
            year=2004,
            seller=other,
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        payload = {"price": "14000.00"}
        response = self.client.patch(f"/api/cars/{car.id}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_car_list_anon_only_active(self):
        Car.objects.create(
            model=self.model,
            generation=self.generation,
            body_type="Sedan",
            vin="1HGBH41JXMN109186",
            owner_count=1,
            price="15000.00",
            mileage=120000,
            year=2004,
            seller=self.user,
            is_active=False,
        )
        response = self.client.get("/api/cars/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_car_list_user_only_active(self):
        Car.objects.create(
            model=self.model,
            generation=self.generation,
            body_type="Sedan",
            vin="1HGBH41JXMN109186",
            owner_count=1,
            price="15000.00",
            mileage=120000,
            year=2004,
            seller=self.user,
            is_active=False,
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get("/api/cars/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_car_list_admin_sees_all(self):
        Car.objects.create(
            model=self.model,
            generation=self.generation,
            body_type="Sedan",
            vin="1HGBH41JXMN109186",
            owner_count=1,
            price="15000.00",
            mileage=120000,
            year=2004,
            seller=self.user,
            is_active=False,
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get("/api/cars/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

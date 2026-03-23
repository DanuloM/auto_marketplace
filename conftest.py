import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='user', email='user@example.com', password='UserPass123!'
    )

@pytest.fixture
def admin():
    return User.objects.create_user(
        username='admin', email='admin@example.com', password='AdminPass123!', role='admin'
    )

@pytest.fixture
def user_token(user):
    return RefreshToken.for_user(user).access_token

@pytest.fixture
def admin_token(admin):
    return RefreshToken.for_user(admin).access_token

@pytest.fixture
def auth_client(api_client, user_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')
    return api_client

@pytest.fixture
def admin_client(api_client, admin_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
    return api_client

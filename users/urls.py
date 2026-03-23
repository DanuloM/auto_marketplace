from django.urls import path
from .views import UserRetrieveUpdateView, UserCreateView

urlpatterns = [
    path('me/', UserRetrieveUpdateView.as_view(), name='user-me'),
    path('register/', UserCreateView.as_view(), name='user-register'),
]
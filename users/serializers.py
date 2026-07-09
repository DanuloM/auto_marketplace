from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "location",
            "name",
        ]

    def create(self, validated_data):
        name = validated_data.pop("name", "")
        if name:
            parts = name.split(" ", 1)
            validated_data["first_name"] = parts[0]
            if len(parts) > 1:
                validated_data["last_name"] = parts[1]

        # Generate username from email if not provided
        if "username" not in validated_data or not validated_data["username"]:
            validated_data["username"] = validated_data["email"].split("@")[0]

        user = User.objects.create_user(**validated_data)
        refresh = RefreshToken.for_user(user)
        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "location",
            "is_verified",
            "role",
        ]
        read_only_fields = ["id", "username", "email", "is_verified", "role"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "location"]

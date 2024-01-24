from rest_framework import serializers
from ..users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "photo",
            "username",
            "firstname",
            "lastname",
            "patronymic",
            "email",
            "position",
            "superior",
            "subordinates",
        ]

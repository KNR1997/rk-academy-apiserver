from rest_framework import serializers

from .base import BaseSerializer
from ...db.models import User


class UserLiteSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'display_name',
            'mobile_number',
            'email',
            'first_name',
            'last_name',
            'full_name',
        ]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'mobile_number',
            'email',
            'display_name',
            'first_name',
            'last_name',
            'is_active',
            'role_name'
        ]

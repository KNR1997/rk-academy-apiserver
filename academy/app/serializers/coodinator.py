from rest_framework import serializers

from academy.app.permissions.base import ROLE
from academy.db.models import User


class CoordinatorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'mobile_number',
            'email',
            'first_name',
            'last_name',
            'display_name',
            'is_active',
        ]


class CoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)
        email = validated_data.pop("email")
        mobile_number = validated_data.pop("mobile_number", None)
        display_name = validated_data.pop("display_name", None)
        password = validated_data.pop("password")

        # Create user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=ROLE.COORDINATOR.value,
            mobile_number=mobile_number,
            display_name=display_name,
        )
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):

        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)
        email = validated_data.pop("email", None)
        mobile_number = validated_data.pop("mobile_number", None)
        display_name = validated_data.pop("display_name", None)

        if first_name is not None:
            instance.first_name = first_name
        if last_name is not None:
            instance.last_name = last_name
        if email is not None:
            instance.email = email
        if mobile_number is not None:
            instance.mobile_number = mobile_number
        if display_name is not None:
            instance.display_name = display_name

        instance.save()
        return instance

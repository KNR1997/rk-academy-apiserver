from django.db import transaction
from rest_framework import serializers

from academy.app.permissions.base import ROLE
from academy.app.serializers.user import UserLiteSerializer
from academy.db.models import Teacher, User, Notification, UserNotification


class TeacherListSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'department', 'user', 'is_active']


class TeacherCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    mobile_number = serializers.CharField(write_only=True)

    class Meta:
        model = Teacher
        fields = "__all__"
        read_only_fields = ["student_number", "user"]

    # --- VALIDATION ---
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    # --- CREATE ---
    def create(self, validated_data):
        with transaction.atomic():
            # Extract fields NOT in Student model
            first_name = validated_data.pop("first_name")
            last_name = validated_data.pop("last_name")
            username = validated_data.pop("username")
            email = validated_data.pop("email")
            password = validated_data.pop("password")
            mobile_number = validated_data.pop("mobile_number")

            # Create user
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                role=ROLE.TEACHER.value,
                mobile_number=mobile_number,
            )
            user.set_password(password)
            user.save()

            notification = Notification.objects.create(
                title="Welcome to RK Academy",
                message=f"We're so glad you're here!",
                type="USER_WELCOME",
                priority="low",
            )

            UserNotification.objects.create(
                notification=notification,
                user=user,
            )

            # Now validated_data ONLY contains Student model fields
            teacher = Teacher.objects.create(user=user, **validated_data)
            return teacher


class TeacherUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)

    # password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Teacher
        fields = "__all__"
        read_only_fields = ["student_number", "user"]

    # --- VALIDATION ---
    def validate_username(self, value):
        user = self.instance.user
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("User with this username already exists.")
        return value

    def validate_email(self, value):
        user = self.instance.user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    # --- UPDATE ---
    def update(self, instance, validated_data):
        """
        instance → Student instance
        instance.user → related User instance
        validated_data → student fields + username/email/password
        """

        user = instance.user

        # Extract user fields
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)
        username = validated_data.pop("username", None)
        email = validated_data.pop("email", None)
        # password = validated_data.pop("password", None)

        # Update User fields
        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if username:
            user.username = username

        if email:
            user.email = email

        # if password:
        #     user.set_password(password)

        user.save()

        # Update Student fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

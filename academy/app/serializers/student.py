import random
import string
import time

from rest_framework import serializers

from academy.app.permissions.base import ROLE
from academy.app.serializers.academic_year import AcademicYearListSerializer
from academy.app.serializers.base import BaseSerializer
from academy.app.serializers.grade_level import GradeLevelListSerializer
from academy.app.serializers.user import UserLiteSerializer
from academy.db.models import Student, User


class StudentListSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer()
    current_grade = GradeLevelListSerializer()
    current_academic_year = AcademicYearListSerializer()

    class Meta:
        model = Student
        fields = [
            'id',
            'student_number',
            'exam_year',
            'date_of_birth',
            'gender',
            'is_active',
            'user',
            'current_grade',
            'current_academic_year',
            'parent_guardian_name',
            'parent_guardian_phone'
        ]


class StudentCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(write_only=True)
    parent_guardian_phone = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ["student_number", "user"]

    # --- VALIDATION ---
    # def validate_username(self, value):
    #     if User.objects.filter(username=value).exists():
    #         raise serializers.ValidationError("Username already exists.")
    #     return value

    def validate_email(self, value):
        # Only validate if email is provided
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def generate_dummy_email(self, first_name, last_name):
        """Generate a dummy email for students who don't provide one"""
        # Clean names to create a base
        base = f"{first_name or 'student'}.{last_name or 'user'}"
        # Remove special characters and spaces
        base = ''.join(c.lower() for c in base if c.isalnum() or c == '.')

        # Add random string to ensure uniqueness
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

        # Try different combinations until we find a unique one
        attempts = [
            f"{base}.{random_suffix}@dummy.student",
            f"{base}{random_suffix}@dummy.student",
            f"student.{random_suffix}@dummy.student",
            f"user.{random_suffix}@dummy.student",
        ]

        for email in attempts:
            if not User.objects.filter(email=email).exists():
                return email

        # Ultimate fallback with timestamp
        timestamp = int(time.time())
        return f"student.{timestamp}.{random_suffix}@dummy.student"

    # --- CREATE ---
    def create(self, validated_data):
        # Extract fields NOT in Student model
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        username = validated_data.pop("username", None)
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # Generate username if not provided
        # if not username:
        #     base_username = f"{first_name.lower()}.{last_name.lower()}".replace(' ', '')
        #     username = base_username
        #     counter = 1
        #     while User.objects.filter(username=username).exists():
        #         username = f"{base_username}{counter}"
        #         counter += 1

        # Generate dummy email if not provided
        if not email:
            email = self.generate_dummy_email(first_name, last_name)

        # Create user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            role=ROLE.STUDENT.value,
            is_email_verified=False,
        )
        user.set_password(password)
        user.save()

        # Now validated_data ONLY contains Student model fields
        student = Student.objects.create(user=user, **validated_data)
        return student


class StudentUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False, allow_null=True, allow_blank=True)
    parent_guardian_phone = serializers.CharField(write_only=True)

    # password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ["student_number", "user"]

    # --- VALIDATION ---
    # def validate_username(self, value):
    #     user = self.instance.user
    #     if User.objects.filter(username=value).exclude(id=user.id).exists():
    #         raise serializers.ValidationError("User with this username already exists.")
    #     return value

    def validate_email(self, value):
        user = self.instance.user
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    def generate_dummy_email(self, first_name, last_name):
        """Generate a dummy email for students who don't provide one"""
        # Clean names to create a base
        base = f"{first_name or 'student'}.{last_name or 'user'}"
        # Remove special characters and spaces
        base = ''.join(c.lower() for c in base if c.isalnum() or c == '.')

        # Add random string to ensure uniqueness
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

        # Try different combinations until we find a unique one
        attempts = [
            f"{base}.{random_suffix}@dummy.student",
            f"{base}{random_suffix}@dummy.student",
            f"student.{random_suffix}@dummy.student",
            f"user.{random_suffix}@dummy.student",
        ]

        for email in attempts:
            if not User.objects.filter(email=email).exists():
                return email

        # Ultimate fallback with timestamp
        timestamp = int(time.time())
        return f"student.{timestamp}.{random_suffix}@dummy.student"

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

        # Generate dummy email if not provided
        if not email:
            email = self.generate_dummy_email(first_name, last_name)

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


class StudentLiteSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer()
    current_grade = GradeLevelListSerializer()
    current_academic_year = AcademicYearListSerializer()

    class Meta:
        model = Student
        fields = [
            'id',
            'student_number',
            'date_of_birth',
            'gender',
            'is_active',
            'user',
            'current_grade',
            'current_academic_year',
            'parent_guardian_name',
            'parent_guardian_phone'
        ]


class StudentSimpleSerializer(BaseSerializer):
    user = UserLiteSerializer()
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = [
            'id',
            'student_number',
            'date_of_birth',
            'gender',
            'is_active',

            'user',
            'full_name',
        ]

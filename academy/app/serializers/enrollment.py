import calendar

from django.utils import timezone
from rest_framework import serializers

from academy.app.serializers.base import BaseSerializer
from academy.app.serializers.course import CourseOfferingListSerializer
from academy.app.serializers.student import StudentListSerializer, StudentLiteSerializer
from academy.db.models import Enrollment, EnrollmentPayment
from academy.db.models.enrollment import EnrollmentStatusType


class EnrollmentSerializer(BaseSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['status']

    def create(self, validated_data):
        validated_data['status'] = EnrollmentStatusType.LOCKED
        validated_data['is_active'] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Keep only 'is_active' if it exists
        is_active = validated_data.get('is_active')

        # Clear all incoming data
        validated_data.clear()

        # Re-assign only is_active
        if is_active is not None:
            validated_data['is_active'] = is_active

        return super().update(instance, validated_data)


class EnrollmentListSerializer(BaseSerializer):
    student = StudentListSerializer()
    course_offering = CourseOfferingListSerializer()

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'status',
            'last_payment_month',
            'last_payment_year',
            'is_active',
            'student',
            'course_offering',
        ]


class CourseOfferingEnrollmentListSerializer(BaseSerializer):
    student = StudentLiteSerializer()

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'status',
            'last_payment_month',
            'last_payment_year',
            'is_active',

            'student'
        ]


class EnrollmentWithPaymentMonthsSerializer(BaseSerializer):
    student = StudentListSerializer()
    course_offering = CourseOfferingListSerializer()
    months = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'course_offering',
            'student',
            'months',
            'is_active',
        ]

    def get_months(self, enrollment):
        """
        Returns:
        {
          jan: { paid: True, amount: 120 },
          feb: { paid: False },
          ...
        }
        """

        # Fetch payments once (important for performance)
        payments = enrollment.enrollment_payments.all()

        # Map payments by month number (1–12)
        payment_map = {
            p.payment_month: p
            for p in payments
            if p.payment_year == enrollment.last_payment_year
        }

        months = {}

        for month in range(1, 13):
            month_key = calendar.month_abbr[month].lower()  # jan, feb, ...

            payment = payment_map.get(month)

            months[month_key] = {
                "paid": payment is not None,
                "amount": payment.amount if payment else None,
                "payment_date": payment.payment_date if payment else None,
            }

        return months


class EnrollmentPaymentSerializer(BaseSerializer):
    class Meta:
        model = EnrollmentPayment
        fields = '__all__'


class EnrollmentPaymentCreateSerializer(BaseSerializer):
    student = serializers.UUIDField(write_only=True)
    enrollment_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = EnrollmentPayment
        fields = '__all__'
        read_only_fields = ['payment_date', 'enrollment']

    def validate(self, attrs):
        enrollment_id = attrs.get("enrollment_id")

        enrollment = Enrollment.objects.filter(pk=enrollment_id).first()

        if not enrollment:
            raise serializers.ValidationError(
                {"course": "Student not enrolled to this course"}
            )

        # save enrollment into serializer instance
        attrs["enrollment"] = enrollment

        # --- NEW DATE VALIDATION ---
        current = timezone.now().date()
        current_month = current.month
        current_year = current.year

        pay_month = attrs["payment_month"]
        pay_year = attrs["payment_year"]

        # Convert both to comparable "year * 12 + month"
        current_value = current_year * 12 + current_month
        pay_value = pay_year * 12 + pay_month

        if pay_value < current_value:
            raise serializers.ValidationError(
                {"payment_month": "Payment month/year cannot be in the past."}
            )

        # Check duplicate payment
        if EnrollmentPayment.objects.filter(
                enrollment=enrollment,
                payment_month=attrs["payment_month"],
                payment_year=attrs["payment_year"],
        ).exists():
            raise serializers.ValidationError(
                {"payment_month": "Already paid for this course"}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("student", None)
        # validated_data.pop("course_offering", None)

        # automatic payment date
        validated_data["payment_date"] = timezone.now().date()

        return EnrollmentPayment.objects.create(**validated_data)


class EnrollmentPaymentListSerializer(BaseSerializer):
    enrollment = EnrollmentListSerializer()

    class Meta:
        model = EnrollmentPayment
        fields = [
            'id',
            'payment_month',
            'payment_year',
            'amount',
            'payment_date',
            'enrollment'
        ]

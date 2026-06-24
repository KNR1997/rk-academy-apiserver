import calendar
from datetime import datetime

from django.utils import timezone
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
    is_active = serializers.SerializerMethodField()

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
        Returns a dictionary of months with payment status and details.
        
        Returns:
        {
            'jan': { 'paid': True, 'amount': 120.00, 'status': 'paid' },
            'feb': { 'paid': False, 'amount': None, 'status': None },
            ...
        }
        """
        # Get current year - we typically only care about current year's payments
        # But you might want to make this configurable or handle multiple years
        current_year = datetime.now().year
        
        # Fetch all charges for this enrollment in the current year
        # You might want to include previous years if your business logic requires it
        charges = enrollment.charges.filter(
            billing_year=current_year
        ).order_by('billing_month')
        
        # Create a map of month -> charge for quick lookup
        # We consider a charge as "paid" only if status is 'paid'
        # You might want to include 'invoiced' or other statuses based on your logic
        charge_map = {
            charge.billing_month: charge 
            for charge in charges
            if charge.billing_month is not None  # Handle null values
        }
        
        months = {}
        
        for month in range(1, 13):
            month_key = calendar.month_abbr[month].lower()  # jan, feb, ...
            charge = charge_map.get(month)
            
            if charge:
                is_paid = charge.status == 'paid'
                months[month_key] = {
                    "paid": is_paid,
                    "amount": str(charge.amount) if charge.amount else None,
                    "status": charge.status,
                    "description": charge.description,
                    "due_date": charge.due_date,
                }
            else:
                months[month_key] = {
                    "paid": False,
                    "amount": None,
                    "status": None,
                    "description": None,
                    "due_date": None,
                }
        
        return months

    def get_is_active(self, enrollment):
        """
        Determine if enrollment is active based on payment history.
        """
        # Option 1: Use the existing is_active field (if you keep it)
        # return enrollment.is_active
        
        # Option 2: Calculate on the fly (recommended)
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Find the most recent paid charge
        last_paid = enrollment.charges.filter(
            status='paid'
        ).order_by('-billing_year', '-billing_month').first()
        
        if not last_paid:
            return False
        
        # Check if the last payment covers the current month
        # Adjust this logic based on your business rules
        if last_paid.billing_year > current_year:
            return True
        elif last_paid.billing_year == current_year:
            return last_paid.billing_month >= current_month
        else:
            return False

# class EnrollmentWithPaymentMonthsSerializer(BaseSerializer):
#     student = StudentListSerializer()
#     course_offering = CourseOfferingListSerializer()
#     months = serializers.SerializerMethodField()

#     class Meta:
#         model = Enrollment
#         fields = [
#             'id',
#             'course_offering',
#             'student',
#             'months',
#             'is_active',
#         ]

#     def get_months(self, enrollment):
#         """
#         Returns:
#         {
#           jan: { paid: True, amount: 120 },
#           feb: { paid: False },
#           ...
#         }
#         """

#         # Fetch payments once (important for performance)
#         payments = enrollment.enrollment_payments.all()

#         # Map payments by month number (1–12)
#         payment_map = {
#             p.payment_month: p
#             for p in payments
#             # if p.payment_year == enrollment.last_payment_year
#             # if p.payment_year == date.
#         }

#         months = {}

#         for month in range(1, 13):
#             month_key = calendar.month_abbr[month].lower()  # jan, feb, ...

#             payment = payment_map.get(month)

#             months[month_key] = {
#                 "paid": payment is not None,
#                 "amount": payment.amount if payment else None,
#                 "payment_date": payment.payment_date if payment else None,
#             }

#         return months


class EnrollmentPaymentSerializer(BaseSerializer):
    class Meta:
        model = EnrollmentPayment
        fields = '__all__'


class PaymentSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    payment_month = serializers.IntegerField()
    payment_year = serializers.IntegerField()


class EnrollmentPaymentCreateSerializer(serializers.Serializer):
    enrollment_id = serializers.UUIDField()
    student = serializers.UUIDField()
    payments = PaymentSerializer(many=True)

    def validate(self, attrs):
        enrollment_id = attrs["enrollment_id"]

        enrollment = Enrollment.objects.filter(
            pk=enrollment_id
        ).first()

        # Enrollment existence
        if not enrollment:
            raise ValidationError({
                "enrollment": ["Enrollment does not exist"]
            })

        # Enrollment active check
        if not enrollment.is_active:
            raise ValidationError({
                "enrollment": ["Enrollment is not active"]
            })

        seen = set()
        errors = {}

        for idx, payment in enumerate(attrs["payments"]):
            key = (
                payment["payment_month"],
                payment["payment_year"],
            )

            if key in seen:
                errors[f"payments.{idx}.payment_month"] = [
                    f"Duplicate month {payment['payment_month']} found in request."
                ]

            seen.add(key)

            already_paid = EnrollmentPayment.objects.filter(
                enrollment=enrollment,
                payment_month=payment["payment_month"],
                payment_year=payment["payment_year"],
            ).exists()

            if already_paid:
                errors[f"payments.{idx}.payment_month"] = [
                    f"Payment already exists for month {payment['payment_month']}, year {payment['payment_year']}."
                ]

        if errors:
            raise ValidationError(errors)

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        enrollment_id = validated_data["enrollment_id"]
        payments = validated_data["payments"]

        enrollment_payments = [
            EnrollmentPayment(
                enrollment_id=enrollment_id,
                payment_month=payment["payment_month"],
                payment_year=payment["payment_year"],
                amount=payment["amount"],
                payment_date=timezone.now().date(),
            )
            for payment in payments
        ]

        EnrollmentPayment.objects.bulk_create(enrollment_payments)

        return enrollment_payments


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

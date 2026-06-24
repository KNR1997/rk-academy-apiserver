from rest_framework import serializers

from academy.db.models import Invoice, InvoiceLineItem, Enrollment
from academy.app.serializers.payment import PaymentListSerializer
from academy.app.serializers.student import StudentSimpleSerializer
from academy.app.serializers.course import CourseOfferingLiteSerializer


class InvoiceEnrollmentDetailsSerializer(serializers.ModelSerializer):
    student = StudentSimpleSerializer()
    course_offering = CourseOfferingLiteSerializer()

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "course_offering",
        ]


class InvoiceListSerializer(serializers.ModelSerializer):
    enrollment = InvoiceEnrollmentDetailsSerializer()

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "issue_date",
            "subtotal",
            "status",
            "enrollment",
        ]


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItem
        fields = [
            "id",
            "charge",
            "description",
            "quantity",
            "unit_price",
            "line_total",
        ]


class InvoiceDetailsSerializer(serializers.ModelSerializer):
    payment = PaymentListSerializer()
    line_items = InvoiceLineItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "issue_date",
            "due_date",
            "subtotal",
            "discount_amount",
            "tax_amount",
            "total_amount",
            "notes",
            "status",

            "payment",
            "line_items"
        ]

# Python imports
from decimal import Decimal

# Django imports
from django.db import transaction

# Third party imports
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

# Module imports
from academy.db.models import Invoice, EnrollmentCharge, Enrollment, InvoiceLineItem


class EnrollmentChargeSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    billing_month = serializers.IntegerField(
        min_value=1,
        max_value=12,
        required=False,
        allow_null=True
    )
    billing_year = serializers.IntegerField(
        required=False,
        allow_null=True
    )


class InvoiceCreateSerializer(serializers.Serializer):
    enrollment_id = serializers.UUIDField()
    issue_date = serializers.DateField()
    due_date = serializers.DateField()
    charges = EnrollmentChargeSerializer(
        many=True
    )

    def validate(self, attrs):

        enrollment = Enrollment.objects.filter(
            pk=attrs["enrollment_id"],
            is_active=True
        ).first()

        if not enrollment:
            raise ValidationError({
                "enrollment": [
                    "Enrollment does not exist or is inactive."
                ]
            })

        attrs["enrollment"] = enrollment

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        enrollment = validated_data["enrollment"]
        charges_data = validated_data["charges"]
        invoice = Invoice.objects.create(
            enrollment=enrollment,
            invoice_number=self._generate_invoice_number(),
            issue_date=validated_data["issue_date"],
            due_date=validated_data["due_date"],
            status="issued"
        )
        subtotal = Decimal("0.00")

        for charge_data in charges_data:
            charge = EnrollmentCharge.objects.create(
                enrollment=enrollment,
                description=charge_data["description"],
                amount=charge_data["amount"],
                billing_month=charge_data.get("billing_month"),
                billing_year=charge_data.get("billing_year"),
                status="invoiced"
            )
            InvoiceLineItem.objects.create(
                invoice=invoice,
                charge=charge,
                description=charge.description,
                quantity=1,
                unit_price=charge.amount,
                line_total=charge.amount
            )
            subtotal += charge.amount

        invoice.subtotal = subtotal
        invoice.total_amount = subtotal
        invoice.save(
            update_fields=[
                "subtotal",
                "total_amount"
            ]
        )

        return invoice

    def _generate_invoice_number(self):
        from django.utils import timezone

        timestamp = timezone.now().strftime("%Y%m%d%H%M%S")

        return f"INV-{timestamp}"

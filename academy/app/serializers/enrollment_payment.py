# Python imports
from decimal import Decimal

# Django imports
from django.db import transaction
from django.db.models import Q

# Third party imports
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        try:
            enrollment = Enrollment.objects.get(pk=attrs["enrollment_id"])
        except Enrollment.DoesNotExist:
            raise ValidationError({
                "enrollment": ["Enrollment does not exist."]
            })

        attrs["enrollment"] = enrollment

        # Validate that no charges are already paid
        self._validate_no_paid_charges(enrollment, attrs["charges"])

        return attrs

    def _validate_no_paid_charges(self, enrollment, charges_data):
        """
        Check if any of the provided charges already have a paid EnrollmentCharge
        for the same enrollment.
        """
        errors = {}
        
        for index, charge_data in enumerate(charges_data):
            # Build filter conditions for existing charges
            filter_conditions = Q(
                enrollment=enrollment,
                status="paid",
                description=charge_data["description"],
                amount=charge_data["amount"]
            )
            
            # Add billing month and year to filter if provided
            if charge_data.get("billing_month"):
                filter_conditions &= Q(billing_month=charge_data["billing_month"])
            if charge_data.get("billing_year"):
                filter_conditions &= Q(billing_year=charge_data["billing_year"])
            
            # Check if a paid charge already exists
            existing_paid_charge = EnrollmentCharge.objects.filter(
                filter_conditions
            ).exists()
            
            if existing_paid_charge:
                # Create error at the charges.index level
                # You can choose which field to attach the error to
                
                # Option 1: Attach to billing_month field
                if charge_data.get("billing_month") or charge_data.get("billing_year"):
                    errors[f"charges.{index}.billing_month"] = [
                        f"Paid EnrollmentCharge already exists for this month "
                        f"(Description: {charge_data['description']}, "
                        f"Amount: {charge_data['amount']})"
                    ]
                else:
                    # Option 2: If no billing month/year, attach to description or fee
                    errors[f"charges.{index}.fee"] = [
                        f"Paid EnrollmentCharge already exists "
                        f"(Description: {charge_data['description']})"
                    ]
        
        if errors:
            raise ValidationError(errors)

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

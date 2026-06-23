# Django imports
from django.db import transaction
from django.utils import timezone

# Third party imports
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

# Module imports
from academy.db.models import Invoice, EnrollmentCharge, Payment


class PaymentCreateSerializer(serializers.Serializer):

    invoice_id = serializers.UUIDField()

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = serializers.CharField(
        max_length=50
    )

    def validate(self, attrs):

        invoice = Invoice.objects.filter(
            pk=attrs["invoice_id"]
        ).first()

        if not invoice:
            raise ValidationError({
                "invoice": [
                    "Invoice does not exist."
                ]
            })

        if invoice.status == "paid":
            raise ValidationError({
                "invoice": [
                    "Invoice is already paid."
                ]
            })

        if attrs["amount"] != invoice.total_amount:
            raise ValidationError({
                "amount": [
                    f"Expected payment amount {invoice.total_amount}"
                ]
            })

        attrs["invoice"] = invoice

        return attrs

    @transaction.atomic
    def create(self, validated_data):

        invoice = validated_data["invoice"]

        payment = Payment.objects.create(
            invoice=invoice,
            payment_number=self._generate_payment_number(),
            amount=validated_data["amount"],
            payment_date=timezone.now().date(),
            payment_method=validated_data["payment_method"],
            status="completed"
        )

        invoice.status = "paid"
        invoice.save(
            update_fields=["status"]
        )

        EnrollmentCharge.objects.filter(
            invoice_line_items__invoice=invoice
        ).update(
            status="paid"
        )

        return payment

    def _generate_payment_number(self):
        from django.utils import timezone

        timestamp = timezone.now().strftime("%Y%m%d%H%M%S")

        return f"PAY-{timestamp}"


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_number",
            "invoice",
            "amount",
            "payment_date",
            "payment_method",
            "transaction_reference",
            "notes",
            "status",
        ]

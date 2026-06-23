# Python imports
from decimal import Decimal

# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class Invoice(BaseModel):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("issued", "Issued"),
        ("paid", "Paid"),
        ("void", "Void"),
    )
    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )
    enrollment = models.ForeignKey(
        "db.Enrollment",
        related_name="invoices",
        on_delete=models.PROTECT
    )
    issue_date = models.DateField()
    due_date = models.DateField()
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    class Meta:
        db_table = "invoice"

    def __str__(self):
        return self.invoice_number


class InvoiceLineItem(BaseModel):
    invoice = models.ForeignKey(
        "db.Invoice",
        related_name="line_items",
        on_delete=models.CASCADE
    )
    charge = models.ForeignKey(
        "db.EnrollmentCharge",
        related_name="invoice_line_items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    description = models.CharField(
        max_length=255
    )
    quantity = models.PositiveIntegerField(
        default=1
    )
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        db_table = "invoice_line_item"

    def __str__(self):
        return self.description

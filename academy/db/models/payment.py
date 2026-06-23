# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class Payment(BaseModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )
    payment_number = models.CharField(
        max_length=50,
        unique=True
    )
    invoice = models.OneToOneField(
        "db.Invoice",
        related_name="payment",
        on_delete=models.PROTECT
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    payment_date = models.DateField()
    payment_method = models.CharField(
        max_length=50
    )
    transaction_reference = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    notes = models.TextField(
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="completed"
    )

    class Meta:
        db_table = "payment"

    def __str__(self):
        return self.payment_number

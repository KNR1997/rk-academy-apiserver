# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class EnrollmentCharge(BaseModel):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("invoiced", "Invoiced"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    )
    enrollment = models.ForeignKey(
        "db.Enrollment",
        related_name="charges",
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    billing_month = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    billing_year = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    due_date = models.DateField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    class Meta:
        db_table = "enrollment_charge"

    def __str__(self):
        return self.description

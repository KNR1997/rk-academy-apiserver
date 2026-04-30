# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class EnrollmentPayment(BaseModel):
    payment_month = models.PositiveIntegerField()
    payment_year = models.PositiveIntegerField()
    amount = models.FloatField()
    payment_date = models.DateField()

    enrollment = models.ForeignKey(
        'db.Enrollment', related_name="enrollment_payments", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        db_table = "enrollment_payment"

    def __str__(self):
        return self.payment_month

from datetime import datetime

# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class EnrollmentStatusType(models.TextChoices):
    ACTIVE = "ACTIVE"
    LOCKED = "LOCKED"


class Enrollment(BaseModel):
    # status = models.CharField(max_length=20, choices=EnrollmentStatusType.choices)
    # last_payment_month = models.PositiveIntegerField(default=0)
    # last_payment_year = models.PositiveIntegerField(default=0)
    # is_active = models.BooleanField(default=False)

    student = models.ForeignKey(
        'db.Student', related_name="enrollments", on_delete=models.SET_NULL, null=True
    )
    course_offering = models.ForeignKey(
        'db.CourseOffering', related_name="enrollments", on_delete=models.SET_NULL, null=True
    )

    @property
    def last_payment_date(self):
        last_paid = self.charges.filter(status='paid').order_by(
            '-billing_year', '-billing_month').first()
        if last_paid:
            return (last_paid.billing_year, last_paid.billing_month)
        return None

    @property
    def is_active(self):
        if not self.last_payment_date:
            return False
        year, month = self.last_payment_date
        current_year, current_month = datetime.now().year, datetime.now().month
        return (year > current_year) or (year == current_year and month >= current_month)

    class Meta:
        db_table = "enrollment"

    # def __str__(self):
    #     return self.course_offering.

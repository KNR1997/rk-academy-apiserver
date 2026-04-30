# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class EnrollmentStatusType(models.TextChoices):
    ACTIVE = "ACTIVE"
    LOCKED = "LOCKED"


class Enrollment(BaseModel):
    status = models.CharField(max_length=20, choices=EnrollmentStatusType.choices)
    last_payment_month = models.PositiveIntegerField(default=0)
    last_payment_year = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    student = models.ForeignKey(
        'db.Student', related_name="enrollments", on_delete=models.SET_NULL, null=True
    )
    course_offering = models.ForeignKey(
        'db.CourseOffering', related_name="enrollments", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        db_table = "enrollment"

    def __str__(self):
        return self.status

# Django imports
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Module imports
from .base import BaseModel


class CourseContent(BaseModel):
    month = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    year = models.PositiveIntegerField()

    course_offering = models.ForeignKey(
        'db.CourseOffering',
        related_name="contents",
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        db_table = "course_content"
        constraints = [
            models.UniqueConstraint(
                fields=["course_offering", "month", "year"],
                name="unique_course_month_year"
            )
        ]

# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class CourseOffering(BaseModel):
    fee = models.FloatField()
    year = models.PositiveIntegerField()
    batch = models.PositiveIntegerField()

    teacher = models.ForeignKey(
        'db.Teacher', on_delete=models.SET_NULL, null=True
    )
    grade_level = models.ForeignKey(
        'db.GradeLevel', related_name="offerings", on_delete=models.SET_NULL, null=True
    )
    course = models.ForeignKey(
        'db.Course', related_name="offerings", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        db_table = "course_offering"
        unique_together = ("course", "grade_level", "year", "batch")

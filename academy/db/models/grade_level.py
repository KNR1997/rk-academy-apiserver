# Django imports
from django.db import models


class GradeLevel(models.Model):
    """Model for grade levels (6, 7, 8, 9, 10, 11)"""
    GRADE_CHOICES = (
        # (6, 'Grade 6'),
        # (7, 'Grade 7'),
        # (8, 'Grade 8'),
        # (9, 'Grade 9'),
        (10, 'Grade 10'),
        (11, 'Grade 11'),
    )

    level = models.IntegerField(choices=GRADE_CHOICES, unique=True)
    name = models.CharField(max_length=20)  # e.g., "Sixth Grade"
    description = models.TextField(blank=True, null=True)
    next_grade = models.OneToOneField(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='previous_grade'
    )

    class Meta:
        ordering = ['level']

    def __str__(self):
        return self.name

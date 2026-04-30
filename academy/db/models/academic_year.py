# Django imports
from django.db import models


class AcademicYear(models.Model):
    """Model to track academic years (e.g., 2024-2025)"""
    name = models.CharField(max_length=20, unique=True)  # e.g., "2024-2025"
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name

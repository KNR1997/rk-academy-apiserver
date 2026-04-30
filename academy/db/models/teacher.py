# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class Teacher(BaseModel):
    department = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField(auto_now_add=True)
    office_location = models.CharField(max_length=50, blank=True, null=True)
    office_hours = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    user = models.OneToOneField(
        'db.User', on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.user.name}"

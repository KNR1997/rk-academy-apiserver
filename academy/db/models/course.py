# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class Course(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    subject = models.ForeignKey(
        'db.Subject', related_name="courses", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        db_table = "course"

    def __str__(self):
        return self.name

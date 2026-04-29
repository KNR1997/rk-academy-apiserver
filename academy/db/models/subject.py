# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class Subject(BaseModel):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        db_table = "subject"

    def __str__(self):
        return self.name

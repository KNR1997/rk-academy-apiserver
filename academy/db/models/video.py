# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class Video(BaseModel):
    title = models.CharField(max_length=255)
    video_url = models.URLField()

    course_content = models.ForeignKey(
        'CourseContent',
        related_name="videos",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "course_content_video"

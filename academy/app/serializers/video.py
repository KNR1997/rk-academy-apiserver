from academy.db.models import Video
from .base import BaseSerializer
from .course_content import CourseContentPageDataSerializer


class VideoPageDataSerializer(BaseSerializer):
    course_content = CourseContentPageDataSerializer()

    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'video_url',
            'video_date',
            'lesson',
            'day',

            'course_content'
        ]

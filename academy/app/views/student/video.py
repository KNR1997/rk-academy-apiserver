# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course_content import VideoLiteSerializer
from academy.app.views.base import BaseAPIView
from academy.db.models import Student, Video

logger = structlog.getLogger(__name__)


class StudentWatchVideoEndpoint(BaseAPIView):
    @allow_permission([ROLE.STUDENT])
    def get(self, request, *args, pk):
        user = request.user
        student = Student.objects.get(user=user)
        logger.info("student_watch_video_requested", student_id=student.id, video_id=self.kwargs.get("pk"),
                    requested_by=request.user.id)

        video = Video.objects.get(pk=pk)

        logger.info("student_watch_video_loaded", student_id=student.id, video_id=self.kwargs.get("pk"),
                    requested_by=request.user.id)
        return Response(VideoLiteSerializer(video).data, status=status.HTTP_200_OK)

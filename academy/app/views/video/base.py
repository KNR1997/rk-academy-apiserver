# Django imports
# Third-part imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course_content import VideoCreateSerializer, VideoListSerializer, VideoUpdateSerializer, \
    VideoLiteSerializer
from academy.app.views.base import BaseViewSet, BaseAPIView
from academy.db.models import Video

logger = structlog.getLogger(__name__)


# Create your views here.
class VideoListCreateAPIEndpoint(BaseViewSet):
    """Video List and Create Endpoint"""

    model = Video
    serializer_class = VideoListSerializer

    search_fields = ['title']
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
            .select_related('course_content',
                            'course_content__course_offering',
                            'course_content__course_offering__course',
                            'course_content__course_offering__grade_level',
                            'course_content__course_offering__course__subject',
                            )
        )

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("video_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        logger.info("video_create_started", requested_by=request.user.id)

        serializer = VideoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        video = serializer.save()

        logger.info("video_created", video_id=video.id, created_by=request.user.id)
        return Response(VideoLiteSerializer(video).data, status=status.HTTP_201_CREATED)


class VideoDetailAPIEndpoint(BaseAPIView):
    """Video Endpoints to update, retrieve and delete endpoint"""

    model = Video
    serializer_class = VideoListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return Video.objects.all()

    @allow_permission([ROLE.ADMIN, ROLE.STUDENT])
    def get(self, request, *args, pk):
        """Retrieve video

        Retrieve details of a specific video.
        """
        logger.info("video_detail_requested", requested_by=request.user.id, role=request.user.role)

        video = (self.get_queryset()
                 .select_related('course_content',
                                 'course_content__course_offering',
                                 'course_content__course_offering__course',
                                 'course_content__course_offering__course__subject',
                                 )
                 .get(pk=pk))

        logger.info("video_detail_loaded", requested_by=request.user.id, role=request.user.role)
        return Response(self.serializer_class(video).data, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def patch(self, request, pk):
        """Update video"""
        logger.info("video_update_started", video_id=pk, requested_by=request.user.id, role=request.user.role)

        video = Video.objects.get(pk=pk)

        serializer = VideoUpdateSerializer(
            video,
            data={**request.data},
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        video = self.get_queryset().filter(pk=serializer.instance.id).first()

        logger.info("video_updated", video_id=pk, requested_by=request.user.id, role=request.user.role)
        return Response(VideoLiteSerializer(video).data, status=status.HTTP_200_OK)


@allow_permission([ROLE.ADMIN])
def delete(self, request, pk):
    """Delete video"""
    logger.info("video_delete_started", video_id=pk, requested_by=request.user.id, role=request.user.role)

    video = self.get_queryset().filter(pk=pk)
    video.delete()

    logger.info("video_deleted", video_id=pk, requested_by=request.user.id, role=request.user.role)
    return Response(status=status.HTTP_204_NO_CONTENT)

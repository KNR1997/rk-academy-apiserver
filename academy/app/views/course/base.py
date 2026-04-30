# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course import CourseListSerializer, CourseSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Course

logger = structlog.getLogger(__name__)


# Create your views here.
class CourseViewSet(BaseViewSet):
    model = Course
    serializer_class = CourseListSerializer

    search_fields = ["name", "slug"]
    filterset_fields = []

    lookup_field = "slug"

    def get_queryset(self):
        queryset =  (
            self.filter_queryset(super().get_queryset().select_related('subject'))
        )
        logger.info("course_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset
    
    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("course_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        logger.info("course_get_requested", requested_by=request.user.id, role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        logger.info("course_create_started", requested_by=request.user.id)

        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        course = serializer.save()
        
        logger.info("course_created", course_id=course.id, course_number=course.slug,
                    created_by=request.user.id)

        output = CourseListSerializer(course, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        logger.info("course_update_requested", requested_by=request.user.id)
        return super().update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        logger.info("course_partial_update_requested", requested_by=request.user.id)
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        logger.info("course_delete_requested", requested_by=request.user.id)
        return super().destroy(request, *args, **kwargs)

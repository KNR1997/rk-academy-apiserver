# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course import CourseOfferingListSerializer, CourseOfferingSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import CourseOffering

logger = structlog.getLogger(__name__)


class CourseOfferingViewSet(BaseViewSet):
    model = CourseOffering
    serializer_class = CourseOfferingListSerializer

    search_fields = ["year", "grade_level__name"]
    ordering_fields = ['course__name', 'batch', 'year', 'created_at']

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset().select_related('course', 'teacher', 'grade_level'))
        )
        logger.info("course_offering_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    def create(self, request, *args, **kwargs):
        logger.info("course_offering_create_started", requested_by=request.user.id)

        course_offering = CourseOffering.objects.filter(
            course=request.data.get("course"),
            grade_level=request.data.get("grade_level"),
            year=request.data.get("year"),
            batch=request.data.get("batch"),
        ).first()

        if course_offering:
            return Response(
                {"batch": "Course Offering already exists."},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = CourseOfferingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_offering = serializer.save()

        logger.info("course_offering_created", course_offering_id=course_offering.id, created_by=request.user.id)
        return Response(CourseOfferingListSerializer(course_offering).data, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("course_offering_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        logger.info("course_offering_get_requested", requested_by=request.user.id, role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        logger.info("course_offering_update_started", course_offering_id=self.kwargs.get("pk"),
                    requested_by=request.user.id)

        course_offering = CourseOffering.objects.filter(
            course=request.data.get("course"),
            grade_level=request.data.get("grade_level"),
            year=request.data.get("year"),
            batch=request.data.get("batch"),
        ).first()

        if course_offering:
            return Response(
                {"batch": "Course Offering already exists."},
                status=status.HTTP_409_CONFLICT,
            )

        course_offering = CourseOffering.objects.get(pk=kwargs["pk"])

        serializer = CourseOfferingSerializer(
            course_offering,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        course_offering = serializer.save()

        logger.info("course_offering_updated", course_offering_id=self.kwargs.get("pk"), requested_by=request.user.id)
        return Response(CourseOfferingListSerializer(course_offering).data, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        logger.info("course_offering_partial_update_requested", course_offering_id=self.kwargs.get("pk"),
                    requested_by=request.user.id, role=request.user.role)
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        logger.info("course_offering_destroy_requested", course_offering_id=self.kwargs.get("pk"),
                    requested_by=request.user.id, role=request.user.role)
        return super().destroy(request, *args, **kwargs)

# Third party imports
import structlog

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.enrollment import CourseOfferingEnrollmentListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Enrollment

logger = structlog.getLogger(__name__)


class CourseOfferingEnrollmentViewSet(BaseViewSet):
    model = Enrollment
    serializer_class = CourseOfferingEnrollmentListSerializer

    search_fields = []
    ordering_fields = []

    def get_queryset(self):
        course_offering_id = self.kwargs.get("course_offering_id")
        queryset = (
            self.filter_queryset(
                super().get_queryset()
                .select_related(
                    'student',
                    'student__user',
                    'student__current_grade',
                    'student__current_academic_year',
                )
                .filter(course_offering_id=course_offering_id)
            )
        )

        logger.info("course_offering_enrollment_queryset_loaded", user_id=self.request.user.id,
                    role=self.request.user.role)
        return queryset

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("course_offering_enrollment_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

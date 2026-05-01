# Third party imports
import structlog

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course import CourseOfferingListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import CourseOffering

logger = structlog.getLogger(__name__)


# Create your views here.
class TeacherCourseOfferingViewSet(BaseViewSet):
    model = CourseOffering
    serializer_class = CourseOfferingListSerializer

    search_fields = ["year", "grade_level__name"]
    filterset_fields = []

    def get_queryset(self):
        user = self.request.user

        # Get the teacher linked to the logged-in user
        teacher = getattr(user, "teacher", None)

        if not teacher:
            return CourseOffering.objects.none()

        queryset = self.filter_queryset(
            super()
            .get_queryset()
            .select_related('course', 'teacher', 'grade_level')
            .filter(teacher=teacher)
        )
        logger.info("teacher_course_offering_queryset_loaded", user_id=self.request.user.id,
                    role=self.request.user.role)
        return queryset

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("teacher_course_offering_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        logger.info("teacher_course_offering_requested", requested_by=request.user.id, role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

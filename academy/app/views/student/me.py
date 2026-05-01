# Third party imports
import structlog
from django.db.models import Q

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course_content import VideoListSerializer
from academy.app.serializers.enrollment import EnrollmentListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Enrollment, Student, Video

logger = structlog.getLogger(__name__)


class StudentMeEnrollmentViewSet(BaseViewSet):
    model = Enrollment
    serializer_class = EnrollmentListSerializer

    search_fields = []
    ordering_fields = []

    def get_queryset(self):
        user = self.request.user
        student = Student.objects.get(user=user)

        queryset = (
            self.filter_queryset(
                super().get_queryset()).filter(student=student)
        )
        logger.info("student_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    @allow_permission([ROLE.STUDENT])
    def list(self, request, *args, **kwargs):
        logger.info("student_me_enrollment_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.STUDENT])
    def retrieve(self, request, *args, **kwargs):
        logger.info("student_me_enrollment_requested", requested_by=request.user.id, role=request.user.role)
        return super().retrieve(request, *args, **kwargs)


class StudentMeEnrollmentVideosViewSet(BaseViewSet):
    model = Video
    serializer_class = VideoListSerializer

    search_fields = ['title']
    ordering_fields = []

    def get_queryset(self):
        enrollment_id = self.kwargs.get('pk')
        enrollment = Enrollment.objects.get(pk=enrollment_id)

        payments = enrollment.enrollment_payments.all()

        if not payments.exists():
            return Video.objects.none()

        query = Q()

        for payment in payments:
            query |= Q(
                course_content__month=payment.payment_month,
                course_content__year=payment.payment_year
            )

        return Video.objects.filter(
            course_content__course_offering=enrollment.course_offering
        ).filter(query)

    @allow_permission([ROLE.STUDENT])
    def list(self, request, *args, **kwargs):
        logger.info("student_me_enrollment_video_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

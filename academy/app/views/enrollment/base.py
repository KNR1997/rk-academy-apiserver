# Third party imports
import structlog
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.enrollment import EnrollmentListSerializer, EnrollmentWithPaymentMonthsSerializer, \
    EnrollmentSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Enrollment, Student, CourseOffering

logger = structlog.getLogger(__name__)


# Create your views here.
class EnrollmentViewSet(BaseViewSet):
    model = Enrollment
    serializer_class = EnrollmentListSerializer

    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
        "course_offering__grade_level__name"
    ]
    ordering_fields = ['is_active', 'created_at']

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset())
            .select_related('student',
                            'course_offering'
                            )
        )
        logger.info("enrollment_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("enrollment_list_requested", requested_by=request.user.id, role=request.user.role)

        queryset = self.filter_queryset(
            Enrollment.objects
            .select_related("student", "course_offering")
            .prefetch_related("enrollment_payments")
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = EnrollmentWithPaymentMonthsSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = EnrollmentWithPaymentMonthsSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        logger.info("enrollment_get_requested", enrollment_id=self.kwargs.get("pk"), requested_by=request.user.id,
                    role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        logger.info("enrollment_create_started", requested_by=request.user.id)

        enrollment = Enrollment.objects.filter(
            student=request.data.get("student"),
            course_offering=request.data.get("course_offering"),
        ).first()

        if enrollment:
            return Response(
                {"course_offering": "The student already enroll to this course."},
                status=status.HTTP_409_CONFLICT,
            )

        student = Student.objects.get(pk=request.data.get("student"))
        course_offering = CourseOffering.objects.get(pk=request.data.get("course_offering"))

        if student.current_grade != course_offering.grade_level:
            return Response(
                {"course_offering": "Invalid course assignment."},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = EnrollmentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save()

        logger.info("enrollment_created", enrollment_id=enrollment.id, created_by=request.user.id)
        return Response(EnrollmentListSerializer(enrollment).data, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        enrollment = Enrollment.objects.get(pk=kwargs["pk"])
        logger.info("enrollment_update_started", enrollment_id=enrollment.id, requested_by=request.user.id)

        serializer = EnrollmentSerializer(
            enrollment,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save()

        logger.info("enrollment_updated", enrollment_id=enrollment.id, created_by=request.user.id)
        return Response(EnrollmentListSerializer(enrollment).data, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        logger.info("enrollment_partial_update_started", enrollment_id=self.kwargs.get("pk"),
                    requested_by=request.user.id)

        super().partial_update(request, *args, **kwargs)

        logger.info("enrollment_partial_updated", enrollment_id=self.kwargs.get("pk"), requested_by=request.user.id)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        enrollment_id = self.kwargs.get("pk")
        logger.info("enrollment_delete_started", enrollment_id=enrollment_id, requested_by=request.user.id)

        super().destroy(request, *args, **kwargs)

        logger.info("enrollment_deleted", enrollment_id=enrollment_id, requested_by=request.user.id)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class EnrollmentPendingPaymentViewSet(BaseViewSet):
    model = Enrollment
    serializer_class = EnrollmentListSerializer

    search_fields = ["student__user__first_name", "student__user__last_name"]
    ordering_fields = ['student__user__first_name', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)

        month = self.request.query_params.get("last_payment_month")
        year = self.request.query_params.get("last_payment_year")

        if month and year:
            month = int(month)
            year = int(year)

            queryset = queryset.filter(
                Q(last_payment_year__lt=year) |
                Q(
                    last_payment_year=year,
                    last_payment_month__lt=month
                )
            )
        logger.info("enrollment_pending_payment_queryset_loaded", user_id=self.request.user.id,
                    role=self.request.user.role)
        return self.filter_queryset(queryset)

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("enrollment_pending_payment_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

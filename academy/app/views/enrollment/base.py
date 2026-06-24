# Third party imports
import structlog
from django.db.models import Q
from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiRequest, inline_serializer

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.enrollment import EnrollmentListSerializer, EnrollmentWithPaymentMonthsSerializer, \
    EnrollmentSerializer
from academy.app.views.base import BaseViewSet, BaseAPIView
from academy.db.models import Enrollment, Student, CourseOffering
from academy.utils.openapi import (
    ID_PARAMETER,
    UNAUTHORIZED_RESPONSE,
    FORBIDDEN_RESPONSE,
    NOT_FOUND_RESPONSE,
    create_paginated_response,
)

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
            .select_related(
                'student',
                'course_offering'       
            )
        )
        logger.info("enrollment_queryset_loaded")
        return queryset

    @extend_schema(
        operation_id="list_enrollments",
        summary="List or retrieve enrollments",
        description="Retrieve all enrollments.",
        tags=["Enrollments"],
        responses={
            200: create_paginated_response(
                EnrollmentWithPaymentMonthsSerializer,
                "PaginatedEnrollmentResponse",
                "Paginated list of enrollments",
                "Paginated Enrollments",
            ),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
        },
    )
    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def list(self, request, *args, **kwargs):
        logger.info("enrollment_list_requested", requested_by=request.user.id, role=request.user.role)

        queryset = self.filter_queryset(
            Enrollment.objects
            .select_related(
                "student",
                "student__current_grade",
                "student__current_academic_year",
                "student__user",
                "course_offering"
            )
            .prefetch_related("charges")
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

    @extend_schema(
        operation_id="get_enrollment",
        summary="Get enrollment",
        description="Get an enrollment by id.",
        tags=["Enrollments"],
        parameters=[ID_PARAMETER],
        responses={
            201: OpenApiResponse(description="Enrollment", response=EnrollmentListSerializer),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
            404: NOT_FOUND_RESPONSE,
        },
    )
    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def retrieve(self, request, *args, **kwargs):
        logger.info("enrollment_get_requested", enrollment_id=self.kwargs.get("pk"), requested_by=request.user.id,
                    role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="create_enrollment",
        summary="Create enrollment",
        description="Create an enrollment",
        tags=["Enrollments"],
        responses={201: OpenApiResponse(
            description="Course created", response=EnrollmentListSerializer)},
        request=OpenApiRequest(request=EnrollmentSerializer),
    )
    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def create(self, request, *args, **kwargs):
        logger.info("enrollment_create_started", requested_by=request.user.id)

        enrollment = Enrollment.objects.filter(
            student=request.data.get("student"),
            course_offering=request.data.get("course_offering"),
        ).first()

        if enrollment:
            raise ValidationError({
                "course_offering": ["The student already enroll to this course"]
            })

        student = Student.objects.get(pk=request.data.get("student"))
        course_offering = CourseOffering.objects.get(pk=request.data.get("course_offering"))

        # if student.current_grade != course_offering.grade_level:
        #     return Response(
        #         {"course_offering": "Invalid course assignment."},
        #         status=status.HTTP_409_CONFLICT,
        #     )

        serializer = EnrollmentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save()

        logger.info("enrollment_created", enrollment_id=enrollment.id, created_by=request.user.id)
        return Response(EnrollmentListSerializer(enrollment).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id="update_enrollment",
        summary="Update enrollment",
        description="Update an enrollment",
        tags=["Enrollments"],
        parameters=[ID_PARAMETER],
        responses={204: OpenApiResponse(
            description="Enrollment updated", response=EnrollmentListSerializer)},
        request=OpenApiRequest(request=EnrollmentSerializer),
    )
    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def update(self, request, *args, **kwargs):
        enrollment = Enrollment.objects.get(pk=kwargs["pk"])
        logger.info("enrollment_update_started", enrollment_id=enrollment.id, requested_by=request.user.id)

        serializer = EnrollmentSerializer(
            enrollment,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info("enrollment_updated", enrollment_id=enrollment.id, created_by=request.user.id)
        return Response(EnrollmentListSerializer(enrollment).data, status=status.HTTP_200_OK)

    # @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    # def partial_update(self, request, *args, **kwargs):
    #     logger.info("enrollment_partial_update_started", enrollment_id=self.kwargs.get("pk"),
    #                 requested_by=request.user.id)

    #     super().partial_update(request, *args, **kwargs)

    #     logger.info("enrollment_partial_updated", enrollment_id=self.kwargs.get("pk"), requested_by=request.user.id)
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        operation_id="delete_enrollment",
        summary="Delete enrollment",
        description="Delete an enrollment",
        tags=["Enrollments"],
        parameters=[ID_PARAMETER],
        responses={204: OpenApiResponse(description="Enrollment deleted")},
    )
    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
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
        logger.info("enrollment_pending_payment_queryset_loaded")
        return self.filter_queryset(queryset)

    @extend_schema(
        operation_id="list_pending_payment_enrollments",
        summary="List or pending payment enrollments",
        description="Retrieve all pending payment enrollments.",
        tags=["Enrollments"],
        responses={
            200: create_paginated_response(
                EnrollmentListSerializer,
                "PaginatedEnrollmentResponse",
                "Paginated list of enrollments",
                "Paginated Enrollments",
            ),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
        },
    )
    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def list(self, request, *args, **kwargs):
        logger.info("enrollment_pending_payment_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)


class EnrollmentAnalyticsEndpoint(BaseAPIView):
    @extend_schema(
        operation_id="enrollment_analytics",
        summary="Enrollment analytics details",
        description="Retrieve enrollment analytics details.",
        tags=["Enrollments"],
        responses={
            200: inline_serializer(
                name="EnrollmentAnalyticsResponse",
                fields={
                    "active_students": serializers.IntegerField(),
                },
            ),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
        },
    )
    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def get(self, request):
        grade_level = request.query_params.get("grade_level")

        queryset = Student.objects.filter(is_active=True)

        if grade_level:
            queryset = queryset.filter(current_grade__name=grade_level)
        
        active_students_count = queryset.count()

        data = {
            "active_students": active_students_count
        }

        return Response(data, status=status.HTTP_200_OK)

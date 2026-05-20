# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiRequest

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course import CourseOfferingListSerializer, CourseOfferingSerializer, \
    CourseOfferingCreateSerializer, CourseOfferingResponseSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import CourseOffering
from academy.utils.openapi import (
    ID_PARAMETER,
    UNAUTHORIZED_RESPONSE,
    FORBIDDEN_RESPONSE,
    NOT_FOUND_RESPONSE,
    create_paginated_response,
)

logger = structlog.getLogger(__name__)


class CourseOfferingViewSet(BaseViewSet):
    model = CourseOffering
    serializer_class = CourseOfferingListSerializer

    search_fields = ["year", "grade_level__name"]
    ordering_fields = ['course__name', 'batch', 'year', 'created_at']

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset().select_related(
                'course', 'teacher', 'grade_level'))
        )
        logger.info("course_offering_queryset_loaded")
        return queryset

    @extend_schema(
        operation_id="create_course_offering",
        summary="Create course offering",
        description="Create a course offering",
        tags=["CourseOfferings"],
        responses={201: OpenApiResponse(
            description="CourseOffering created", response=CourseOfferingResponseSerializer)},
        request=OpenApiRequest(request=CourseOfferingCreateSerializer),
    )
    def create(self, request, *args, **kwargs):
        logger.info("course_offering_create_started",
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

        serializer = CourseOfferingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_offering = serializer.save()

        logger.info("course_offering_created",
                    course_offering_id=course_offering.id, created_by=request.user.id)
        return Response(CourseOfferingResponseSerializer(course_offering).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id="list_course_offerings",
        summary="List or retrieve course offerings",
        description="Retrieve all course offerings.",
        tags=["CourseOfferings"],
        responses={
            200: create_paginated_response(
                CourseOfferingListSerializer,
                "PaginatedCourseOfferingResponse",
                "Paginated list of course offerings",
                "Paginated Course offerings",
            ),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
        },
    )
    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def list(self, request, *args, **kwargs):
        logger.info("course_offering_list_requested",
                    requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="get_course_offering",
        summary="Get course offering",
        description="Get a course offering by id.",
        tags=["CourseOfferings"],
        parameters=[ID_PARAMETER],
        responses={
            201: OpenApiResponse(description="CourseOffering", response=CourseOfferingListSerializer),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
            404: NOT_FOUND_RESPONSE,
        },
    )
    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        logger.info("course_offering_get_requested",
                    requested_by=request.user.id, role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="update_course_offering",
        summary="Update course offering",
        description="Update a course offering by id.",
        tags=["CourseOfferings"],
        parameters=[ID_PARAMETER],
        responses={204: OpenApiResponse(
            description="CourseOffering updated", response=CourseOfferingResponseSerializer)},
        request=OpenApiRequest(request=CourseOfferingSerializer),
    )
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

        logger.info("course_offering_updated", course_offering_id=self.kwargs.get(
            "pk"), requested_by=request.user.id)
        return Response(CourseOfferingResponseSerializer(course_offering).data, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        logger.info("course_offering_partial_update_requested", course_offering_id=self.kwargs.get("pk"),
                    requesteID_PARAMETERd_by=request.user.id, role=request.user.role)
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="delete_course_offering",
        summary="Delete course offering",
        description="Delete a course offering by id.",
        tags=["CourseOfferings"],
        parameters=[ID_PARAMETER],
        responses={204: OpenApiResponse(description="CourseOffering deleted")},
    )
    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        logger.info("course_offering_destroy_requested", course_offering_id=self.kwargs.get("pk"),
                    requested_by=request.user.id, role=request.user.role)
        return super().destroy(request, *args, **kwargs)

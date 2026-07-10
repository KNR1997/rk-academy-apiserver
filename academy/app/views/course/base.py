# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiRequest

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.course import CourseResponseSerializer, CourseCreateSerializer, CourseUpdateSerializer, CourseLiteSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Course
from academy.utils.openapi import (
    ID_PARAMETER,
    COURSE_SLUG_PARAMETER,
    UNAUTHORIZED_RESPONSE,
    FORBIDDEN_RESPONSE,
    NOT_FOUND_RESPONSE,
    create_paginated_response,
)

logger = structlog.getLogger(__name__)


# Create your views here.
class CourseViewSet(BaseViewSet):
    model = Course
    serializer_class = CourseResponseSerializer

    search_fields = ["name", "slug"]
    ordering_fields = ['name', 'slug', 'created_at']

    lookup_field = "slug"

    def get_queryset(self):
        queryset = (
            self.filter_queryset(
                super().get_queryset().select_related('subject'))
        )
        logger.info("course_queryset_loaded")
        return queryset

    @extend_schema(
        operation_id="list_courses",
        summary="List or retrieve courses",
        description="Retrieve all courses.",
        tags=["Courses"],
        responses={
            200: create_paginated_response(
                CourseResponseSerializer,
                "PaginatedCourseResponse",
                "Paginated list of courses",
                "Paginated Courses",
            ),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
        },
    )
    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("course_list_requested",
                    requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="get_course",
        summary="Get course",
        description="Get a course by slug.",
        tags=["Courses"],
        parameters=[COURSE_SLUG_PARAMETER],
        responses={
            201: OpenApiResponse(description="Course", response=CourseResponseSerializer),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
            404: NOT_FOUND_RESPONSE,
        },
    )
    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        logger.info("course_get_requested",
                    requested_by=request.user.id, role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="create_course",
        summary="Create course",
        description="Create a course",
        tags=["Courses"],
        responses={201: OpenApiResponse(
            description="Course created", response=CourseResponseSerializer)},
        request=OpenApiRequest(request=CourseCreateSerializer),
    )
    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        logger.info("course_create_started", requested_by=request.user.id)

        serializer = CourseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = serializer.save()

        logger.info("course_created", course_id=course.id, course_number=course.slug,
                    created_by=request.user.id)

        output = CourseLiteSerializer(
            course, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id="update_course",
        summary="Update course",
        description="Update a course",
        tags=["Courses"],
        parameters=[COURSE_SLUG_PARAMETER],
        responses={204: OpenApiResponse(
            description="Course updated", response=CourseLiteSerializer)},
        request=OpenApiRequest(request=CourseUpdateSerializer),
    )
    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        logger.info("course_update_started", course_slug=self.kwargs.get(
            'slug'), requested_by=request.user.id)

        course = Course.objects.get(slug=kwargs["slug"])
        serializer = CourseUpdateSerializer(
            course,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        course = serializer.save()

        logger.info("course_updated", subject_slug=self.kwargs.get(
            'slug'), created_by=request.user.id)
        return Response(CourseLiteSerializer(course).data, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id="delete_course",
        summary="Delete course",
        description="Delete a course",
        tags=["Courses"],
        parameters=[ID_PARAMETER],
        responses={204: OpenApiResponse(description="Course deleted")},
    )
    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        logger.info("course_delete_requested", course_slug=self.kwargs.get(
            'slug'), requested_by=request.user.id)

        course = Course.objects.get(slug=kwargs.get("slug"))
        course.delete(soft=False)

        logger.info("subject_deleted", course_slug=self.kwargs.get(
            'slug'), requested_by=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

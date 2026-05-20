# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiRequest

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.teacher import TeacherListSerializer, TeacherCreateSerializer, TeacherUpdateSerializer, TeacherLiteSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Teacher
from academy.utils.openapi import (
    ID_PARAMETER,
    UNAUTHORIZED_RESPONSE,
    FORBIDDEN_RESPONSE,
    TEACHER_NOT_FOUND_RESPONSE,
    create_paginated_response,
)

logger = structlog.getLogger(__name__)


class TeacherViewSet(BaseViewSet):
    model = Teacher
    serializer_class = TeacherListSerializer

    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    ordering_fields = ['user__first_name', 'is_active', 'created_at']

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset().select_related('user'))
        )
        logger.info("teacher_queryset_loaded")
        return queryset

    @extend_schema(
        operation_id="list_teachers",
        summary="List or retrieve teachers",
        description="Retrieve all teachers.",
        tags=["Teachers"],
        parameters=[],
        responses={
            200: create_paginated_response(
                TeacherListSerializer,
                "PaginatedTeacherResponse",
                "Paginated list of teachers",
                "Paginated Teachers",
            ),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
        },
    )
    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("teacher_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="get_teacher",
        summary="Get teacher",
        description="Get a teacher by slug.",
        tags=["Teachers"],
        parameters=[ID_PARAMETER],
        responses={
            201: OpenApiResponse(description="Teacher", response=TeacherListSerializer),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
            404: TEACHER_NOT_FOUND_RESPONSE,
        },
    )
    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        logger.info("teacher_retrieve_requested", requested_by=request.user.id, role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="create_teacher",
        summary="Create teacher",
        description="Create a teacher",
        tags=["Teachers"],
        responses={201: OpenApiResponse(
            description="Teacher created", response=TeacherLiteSerializer)},
        request=OpenApiRequest(request=TeacherCreateSerializer),
    )
    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        logger.info("teacher_create_started", requested_by=request.user.id)

        serializer = TeacherCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        teacher = serializer.save()

        logger.info("teacher_created", teacher_id=teacher.id, created_by=request.user.id)
        return Response(TeacherLiteSerializer(teacher).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id="update_teacher",
        summary="Update teacher",
        description="Update a teacher",
        tags=["Teachers"],
        parameters=[ID_PARAMETER],
        responses={204: OpenApiResponse(
            description="Teacher updated", response=TeacherLiteSerializer)},
        request=OpenApiRequest(request=TeacherUpdateSerializer),
    )
    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        logger.info("teacher_update_started", teacher_id=self.kwargs.get('pk'), requested_by=request.user.id)

        teacher = Teacher.objects.get(pk=kwargs["pk"])
        serializer = TeacherUpdateSerializer(
            teacher,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.info("teacher_updated", teacher_id=teacher.id, created_by=request.user.id)
        return Response(TeacherLiteSerializer(teacher).data, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id="delete_teacher",
        summary="Delete teacher",
        description="Delete a teacher by id",
        tags=["Teachers"],
        parameters=[ID_PARAMETER],
        responses={204: OpenApiResponse(description="Teacher deleted")},
    )
    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        logger.info("teacher_delete_requested", teacher_id=self.kwargs.get('pk'), requested_by=request.user.id)

        teacher = Teacher.objects.get(pk=kwargs.get("pk"))
        teacher.delete(soft=False)

        logger.info("teacher_deleted", teacher_id=self.kwargs.get('pk'), requested_by=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

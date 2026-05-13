# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiRequest

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.subject import SubjectResponseSerializer, SubjectCreateSerializer, SubjectUpdateSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Subject
from academy.utils.openapi import (
    SUBJECT_SLUG_PARAMETER,
    UNAUTHORIZED_RESPONSE,
    FORBIDDEN_RESPONSE,
    SUBJECT_NOT_FOUND_RESPONSE,
    create_paginated_response,
)

logger = structlog.getLogger(__name__)


# Create your views here.
class SubjectViewSet(BaseViewSet):
    model = Subject
    serializer_class = SubjectResponseSerializer

    search_fields = ["name", "slug"]
    filterset_fields = []

    lookup_field = "slug"

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset())
        )
        logger.info("subject_queryset_loaded")
        return queryset

    @extend_schema(
        operation_id="create_subject",
        summary="Create subject",
        description="Create a subject",
        tags=["Subjects"],
        responses={201: OpenApiResponse(description="Subject created", response=SubjectResponseSerializer)},
        request=OpenApiRequest(request=SubjectCreateSerializer),
    )
    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        logger.info("subject_create_started", requested_by=request.user.id, role=request.user.role)

        serializer = SubjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subject = serializer.save()

        logger.info("subject_created", requested_by=request.user.id, role=request.user.role)
        return Response(SubjectResponseSerializer(subject).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id="list_subjects",
        summary="List or retrieve subjects",
        description="Retrieve all subjects.",
        tags=["Subjects"],
        parameters=[],
        responses={
            200: create_paginated_response(
                SubjectResponseSerializer,
                "PaginatedSubjectResponse",
                "Paginated list of subjects",
                "Paginated Subjects",
            ),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
        },
    )
    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("subject_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @extend_schema(
        operation_id="get_subject",
        summary="Get subject",
        description="Get a subject by slug.",
        tags=["Subjects"],
        parameters=[SUBJECT_SLUG_PARAMETER],
        responses={
            201: OpenApiResponse(description="Subject", response=SubjectResponseSerializer),
            401: UNAUTHORIZED_RESPONSE,
            403: FORBIDDEN_RESPONSE,
            404: SUBJECT_NOT_FOUND_RESPONSE,
        },
    )
    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        logger.info("subject_retrieve_requested", requested_by=request.user.id, role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="update_subject",
        summary="Update subject",
        description="Update a subject",
        tags=["Subjects"],
        parameters=[SUBJECT_SLUG_PARAMETER],
        responses={204: OpenApiResponse(description="Subject updated", response=SubjectResponseSerializer)},
        request=OpenApiRequest(request=SubjectUpdateSerializer),
    )
    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        logger.info("subject_update_started", subject_slug=self.kwargs.get('slug'), requested_by=request.user.id)

        subject = Subject.objects.get(slug=kwargs["slug"])
        serializer = SubjectUpdateSerializer(
            subject,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        subject = serializer.save()

        logger.info("subject_updated", subject_slug=self.kwargs.get('slug'), created_by=request.user.id)
        return Response(SubjectResponseSerializer(subject).data, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id="delete_subject",
        summary="Delete subject",
        description="Delete a subject by slug",
        tags=["Subjects"],
        parameters=[SUBJECT_SLUG_PARAMETER],
        responses={204: OpenApiResponse(description="Subject deleted")},
    )
    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        logger.info("subject_delete_requested", subject_slug=self.kwargs.get('slug'), requested_by=request.user.id)

        subject = Subject.objects.get(slug=kwargs.get("slug"))
        subject.delete(soft=False)

        logger.info("subject_deleted", subject_slug=self.kwargs.get('slug'), requested_by=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

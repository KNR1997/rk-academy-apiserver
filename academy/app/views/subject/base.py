# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.subject import SubjectResponseSerializer, SubjectCreateSerializer, SubjectUpdateSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Subject

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
        logger.info("subject_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    @extend_schema(
        request=SubjectCreateSerializer,
        responses={
            201: OpenApiResponse(
                description="Subject created successfully",
                response=SubjectResponseSerializer,
            ),
            400: OpenApiResponse(description="Validation error"),
        },
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "name": "Maths",
                    "slug": "maths",
                    "code": "mat",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example Response",
                value={
                    "id": "8c5ba230-5672-4c18-bf25-5a0b8a38c85d",
                    "name": "Maths",
                    "slug": "maths",
                    "code": "mat",
                },
                response_only=True,
            ),
        ],
        description="Create a new subject",
        summary="Create Subject"
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
        responses={
            200: OpenApiResponse(
                description="Subjects get successfully",
                response=SubjectResponseSerializer,
            ),
        },
        examples=[
            OpenApiExample(
                "Example SubjectResponseSerializer",
                value={
                    "name": "Maths",
                    "slug": "maths",
                    "code": "mat",
                },
                response_only=True,
            ),
        ],
        summary="Get paginated Subjects"
    )
    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("subject_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Subject get successfully",
                response=SubjectResponseSerializer,
            ),
        },
        examples=[
            OpenApiExample(
                "Example SubjectResponseSerializer",
                value={
                    "id": "8c5ba230-5672-4c18-bf25-5a0b8a38c85d",
                    "name": "Maths",
                    "slug": "maths",
                    "code": "mat",
                },
                response_only=True,
            ),
        ],
        summary="Get Subject by slug"
    )
    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        logger.info("subject_retrieve_requested", requested_by=request.user.id, role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        request=SubjectUpdateSerializer,
        responses={
            200: OpenApiResponse(
                description="Subject updated successfully",
                response=SubjectResponseSerializer,
            ),
            400: OpenApiResponse(description="Validation error"),
        },
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "name": "Maths",
                    "slug": "maths",
                    "code": "mat",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example Response",
                value={
                    "id": "8c5ba230-5672-4c18-bf25-5a0b8a38c85d",
                    "name": "Maths",
                    "slug": "maths",
                    "code": "mat",
                },
                response_only=True,
            ),
        ],
        description="Update a subject",
        summary="Update Subject by slug"
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
        responses={
            200: OpenApiResponse(
                description="Subject deleted successfully",
                response=SubjectResponseSerializer,
            ),
            404: OpenApiResponse(description="Subject not found error"),
        },
        description="Delete a subject",
        summary="Delete Subject by slug"
    )
    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        logger.info("subject_delete_requested", subject_id=self.kwargs.get('pk'), requested_by=request.user.id)

        super().destroy(request, *args, **kwargs)

        logger.info("subject_deleted", subject_id=self.kwargs.get('pk'), requested_by=request.user.id)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

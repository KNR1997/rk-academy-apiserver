# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.subject import SubjectListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Subject

logger = structlog.getLogger(__name__)


# Create your views here.
class SubjectViewSet(BaseViewSet):
    model = Subject
    serializer_class = SubjectListSerializer

    search_fields = ["name", "slug"]
    filterset_fields = []

    lookup_field = "slug"

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset())
        )
        logger.info("subject_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        logger.info("subject_create_started", requested_by=request.user.id, role=request.user.role)

        super().create(request, *args, **kwargs)

        logger.info("subject_created", requested_by=request.user.id, role=request.user.role)
        return Response(None, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("subject_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        logger.info("subject_retrieve_requested", requested_by=request.user.id, role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        logger.info("subject_update_started", subject_id=self.kwargs.get('pk'), requested_by=request.user.id)

        super().update(request, *args, **kwargs)

        logger.info("subject_updated", subject_id=self.kwargs.get('pk'), created_by=request.user.id)
        return Response(None, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        logger.info("subject_partial_update_requested", subject_id=self.kwargs.get('pk'), requested_by=request.user.id)

        super().partial_update(request, *args, **kwargs)

        logger.info("subject_partial_updated", subject_id=self.kwargs.get('pk'), requested_by=request.user.id)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        logger.info("subject_delete_requested", subject_id=self.kwargs.get('pk'), requested_by=request.user.id)

        super().destroy(request, *args, **kwargs)

        logger.info("subject_deleted", subject_id=self.kwargs.get('pk'), requested_by=request.user.id)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

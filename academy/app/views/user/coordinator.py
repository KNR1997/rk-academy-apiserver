# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import ROLE, allow_permission
from academy.app.serializers.coodinator import CoordinatorSerializer, CoordinatorListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import User

logger = structlog.getLogger(__name__)


class CoordinatorViewSet(BaseViewSet):
    model = User
    serializer_class = CoordinatorListSerializer

    search_fields = ["username", "email"]
    ordering_fields = ['first_name', 'created_at']

    def get_queryset(self):
        queryset = (
            self.filter_queryset(
                super().get_queryset().filter(
                    role=ROLE.COORDINATOR.value
                )
            )
        )
        logger.info("coordinator_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("coordinator_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        logger.info("coordinator_create_started", requested_by=request.user.id)

        serializer = CoordinatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        coordinator = serializer.save()

        logger.info("coordinator_created", coordinator_id=coordinator.id, created_by=request.user.id)
        return Response(CoordinatorListSerializer(coordinator).data, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        logger.info("coordinator_update_started", requested_by=request.user.id)

        coordinator = User.objects.get(pk=kwargs["pk"])
        serializer = CoordinatorSerializer(
            coordinator,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        coordinator = serializer.save()

        logger.info("coordinator_updated", coordinator_id=coordinator.id, created_by=request.user.id)
        return Response(CoordinatorListSerializer(coordinator).data, status=status.HTTP_200_OK)

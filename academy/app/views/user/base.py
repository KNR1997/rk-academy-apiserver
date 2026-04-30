# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.user import UserListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import User

logger = structlog.getLogger(__name__)


class UserViewSet(BaseViewSet):
    model = User
    serializer_class = UserListSerializer

    search_fields = ["username", "email"]
    ordering_fields = ['first_name', 'is_active', 'created_at']

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset())
        )
        logger.info("user_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("user_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        logger.info("user_delete_requested", requested_by=request.user.id)
        return super().destroy(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def deactivate(self, request, *args, **kwargs):
        logger.info("user_account_deactivate_started", requested_by=request.user.id)

        deactivate_user_id = request.data['id']
        user = User.objects.get(id=deactivate_user_id)

        # Deactivate the user
        user.is_active = False
        user.save()

        logger.info("user_account_deactivate_completed", user_id=user.id, created_by=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

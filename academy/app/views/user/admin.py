# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import ROLE, allow_permission
from academy.app.serializers.authentication import ResetTeacherPasswordSerializer
from academy.app.serializers.user import UserListSerializer
from academy.app.views.base import BaseViewSet, BaseAPIView
from academy.db.models import User, Teacher

logger = structlog.getLogger(__name__)


class AdminViewSet(BaseViewSet):
    model = User
    serializer_class = UserListSerializer

    search_fields = ["username", "email"]

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset().filter(role=ROLE.ADMIN.value))
        )
        logger.info("user_admin_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("admin_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)


class ResetTeacherPasswordEndpoint(BaseAPIView):
    @allow_permission([ROLE.ADMIN])
    def post(self, request, *args, **kwargs):
        logger.info("admin_rest_teacher_password_started", requested_by=request.user.id)

        serializer = ResetTeacherPasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        teacher_id = self.kwargs.get("teacher_id")

        teacher = Teacher.objects.get(pk=teacher_id)

        user = teacher.user
        user.set_password(serializer.validated_data.get("password"))

        user.save()

        logger.info("admin_rest_teacher_password_completed", teacher_id=teacher_id, created_by=request.user.id)
        return Response(status=status.HTTP_200_OK)

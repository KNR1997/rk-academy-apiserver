# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.teacher import TeacherListSerializer, TeacherCreateSerializer, TeacherUpdateSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Teacher

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
        logger.info("course_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("teacher_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        logger.info("teacher_create_started", requested_by=request.user.id)

        serializer = TeacherCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        teacher = serializer.save()

        logger.info("teacher_created", teacher_id=teacher.id, created_by=request.user.id)
        return Response(TeacherListSerializer(teacher).data, status=status.HTTP_201_CREATED)

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
        teacher = serializer.save()

        logger.info("teacher_updated", teacher_id=teacher.id, created_by=request.user.id)
        return Response(TeacherListSerializer(teacher).data, status=status.HTTP_200_OK)

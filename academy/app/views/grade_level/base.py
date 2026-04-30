# Third party imports
import structlog

# Module imports
from academy.app.serializers.grade_level import GradeLevelListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import GradeLevel

logger = structlog.getLogger(__name__)


# Create your views here.
class GradeLevelViewSet(BaseViewSet):
    model = GradeLevel
    serializer_class = GradeLevelListSerializer

    search_fields = ["level"]
    filterset_fields = []

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset())
        )
        logger.info("grade_level_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    def create(self, request, *args, **kwargs):
        logger.info("grade_level_create_requested", requested_by=request.user.id)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        logger.info("grade_level_list_requested", requested_by=request.user.id)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("grade_level_retrieve_requested", grade_level_id=self.kwargs.get('pk'),
                    requested_by=request.user.id)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info("grade_level_update_requested", grade_level_id=self.kwargs.get('pk'), requested_by=request.user.id)
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.info("grade_level_partial_update_requested", grade_level_id=self.kwargs.get('pk'),
                    requested_by=request.user.id)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info("grade_level_destroy_requested", grade_level_id=self.kwargs.get('pk'), requested_by=request.user.id)
        return super().destroy(request, *args, **kwargs)

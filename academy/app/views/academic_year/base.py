# Third party imports
import structlog

# Module imports
from academy.app.serializers.academic_year import AcademicYearListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import AcademicYear

logger = structlog.getLogger(__name__)


# Create your views here.
class AcademicYearViewSet(BaseViewSet):
    model = AcademicYear
    serializer_class = AcademicYearListSerializer

    search_fields = ["name"]
    filterset_fields = []

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset())
        )
        logger.info("academic_year_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    def create(self, request, *args, **kwargs):
        logger.info("academic_year_create_requested", requested_by=request.user.id, role=request.user.role)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        logger.info("academic_year_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("academic_year_get_requested", academic_year_id=self.kwargs.get('pk'), requested_by=request.user.id,
                    role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info("academic_year_update_requested", academic_year_id=self.kwargs.get('pk'),
                    requested_by=request.user.id, role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.info("academic_year_partial_update_requested", academic_year_id=self.kwargs.get('pk'),
                    requested_by=request.user.id, role=request.user.role)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info("academic_year_destroy_requested", academic_year_id=self.kwargs.get('pk'),
                    requested_by=request.user.id, role=request.user.role)
        return super().destroy(request, *args, **kwargs)

# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.views.base import BaseAPIView
from academy.db.models import Student, Enrollment
from academy.db.models.enrollment import EnrollmentStatusType

logger = structlog.getLogger(__name__)


# Create your views here.
class InstituteAnalyticsDataEndpoint(BaseAPIView):
    def get(self, request):
        logger.info("institute_analytics_requested", requested_by=request.user.id, role=request.user.role)

        student_count = Student.objects.all().count()
        enrollment_count = Enrollment.objects.all().count()
        active_enrollment_count = Enrollment.objects.filter(status=EnrollmentStatusType.ACTIVE).count()

        output = {
            "total_revenue": 0,
            "student_count": student_count,
            "enrollment_count": enrollment_count,
            "active_enrollment_count": active_enrollment_count,
        }

        logger.info("institute_analytics_loaded", requested_by=request.user.id, role=request.user.role)
        return Response(output, status=status.HTTP_200_OK)

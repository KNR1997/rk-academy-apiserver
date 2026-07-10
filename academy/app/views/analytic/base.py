# Python imports
from calendar import month_name

# Django imports
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone

# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.views.base import BaseAPIView
from academy.db.models import Student, Enrollment

logger = structlog.getLogger(__name__)


# Create your views here.
class InstituteAnalyticsDataEndpoint(BaseAPIView):
    def get(self, request):
        logger.info("institute_analytics_requested",
                    requested_by=request.user.id, role=request.user.role)

        student_count = Student.objects.all().count()
        enrollment_count = Enrollment.objects.all().count()

        # Get enrollments by month for the current year
        current_year = timezone.now().year
        enrollments_by_month = (
            Enrollment.objects
            .filter(created_at__year=current_year)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('month')
        )

        # Create a dict for easy lookup
        enrollments_dict = {entry['month'].month: entry['total'] for entry in enrollments_by_month}

        # Fill in all months (including those with 0 enrollments)
        formatted_enrollments_by_month = []
        for month_num in range(1, 13):
            formatted_enrollments_by_month.append({
                'month': month_name[month_num],
                'total': enrollments_dict.get(month_num, 0)
            })

        # active_enrollment_count = Enrollment.objects.filter(is_active=True).count()

        output = {
            "total_revenue": 0,
            "student_count": student_count,
            "enrollment_count": enrollment_count,
            "active_enrollment_count": enrollment_count,
            "enrollments_by_month": formatted_enrollments_by_month,
        }

        logger.info("institute_analytics_loaded",
                    requested_by=request.user.id, role=request.user.role)
        return Response(output, status=status.HTTP_200_OK)

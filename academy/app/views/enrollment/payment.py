# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Django imports
from django.db import transaction

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.enrollment import EnrollmentPaymentListSerializer, EnrollmentPaymentCreateSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import EnrollmentPayment
from academy.db.models.enrollment import EnrollmentStatusType

logger = structlog.getLogger(__name__)


# Create your views here.
class EnrollmentPaymentViewSet(BaseViewSet):
    model = EnrollmentPayment
    serializer_class = EnrollmentPaymentListSerializer

    search_fields = [
        "enrollment__student__user__first_name",
        "enrollment__student__user__last_name"
    ]
    ordering_fields = [
        'enrollment__student__user__first_name',
        'created_at'
    ]

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset().select_related('enrollment'))
        )
        logger.info("enrollment_payment_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            logger.info("enrollment_payment_create_started", requested_by=request.user.id)

            serializer = EnrollmentPaymentCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            enrollment_payment = serializer.save()

            enrollment = enrollment_payment.enrollment

            enrollment.last_payment_month = enrollment_payment.payment_month
            enrollment.last_payment_year = enrollment_payment.payment_year
            enrollment.status = EnrollmentStatusType.ACTIVE

            enrollment.save()

            logger.info("enrollment_payment_created", enrollment_payment_id=enrollment_payment.id,
                        enrollment_id=enrollment.id, created_by=request.user.id)
            return Response(EnrollmentPaymentListSerializer(enrollment_payment).data, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        logger.info("enrollment_payment_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        logger.info("enrollment_payment_requested", enrollment_payment_id=self.kwargs.get("pk"),
                    requested_by=request.user.id,
                    role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        logger.info("enrollment_payment_update_started", enrollment_payment_id=self.kwargs.get("pk"),
                    requested_by=request.user.id,
                    role=request.user.role)

        output = super().update(request, *args, **kwargs)

        logger.info("enrollment_payment_updated", enrollment_payment_id=self.kwargs.get("pk"),
                    requested_by=request.user.id,
                    role=request.user.role)
        return Response(output, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        logger.info("enrollment_payment_partial_update_started", enrollment_payment_id=self.kwargs.get("pk"),
                    requested_by=request.user.id, role=request.user.role)

        output = super().partial_update(request, *args, **kwargs)

        logger.info("enrollment_payment_partial_updated", enrollment_payment_id=self.kwargs.get("pk"),
                    requested_by=request.user.id,
                    role=request.user.role)
        return Response(output, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        logger.info("enrollment_payment_delete_started", enrollment_id=self.kwargs.get("pk"),
                    requested_by=request.user.id,
                    role=request.user.role)

        super().destroy(request, *args, **kwargs)

        logger.info("enrollment_payment_deleted", enrollment_payment_id=self.kwargs.get("pk"),
                    requested_by=request.user.id,
                    role=request.user.role)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

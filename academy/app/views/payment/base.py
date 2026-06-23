# Django imports

# Third party imports
import structlog
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.views.base import BaseAPIView
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.payment import PaymentCreateSerializer

logger = structlog.getLogger(__name__)


class PaymentCreateAPIEndpoint(BaseAPIView):
    """Payment Endpoints to create"""

    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def post(self, request):
        logger.info("payment_create_started", requested_by=request.user.id)

        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save()

        logger.info("payment_created", payment_id=payment.id,
                    created_by=request.user.id)
        return Response(None, status=status.HTTP_201_CREATED)

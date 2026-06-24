# Django imports
from django.http import HttpResponse

# Third-part imports
import structlog
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.invoice import InvoiceListSerializer, InvoiceDetailsSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Invoice, Payment
from academy.app.services.invoice_pdf_service import InvoicePdfService

logger = structlog.getLogger(__name__)


class InvoiceViewSet(BaseViewSet):
    model = Invoice
    serializer_class = InvoiceListSerializer

    search_fields = []
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = (
            self.filter_queryset(super().get_queryset())
            .select_related(
                'enrollment',
                'enrollment__student',
                "enrollment__student__user",
                'enrollment__course_offering',
                "enrollment__course_offering__grade_level",
                "enrollment__course_offering__course",
                "enrollment__course_offering__course__subject",
            )
        )
        logger.info("invoice_queryset_loaded")
        return queryset

    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def list(self, request, *args, **kwargs):
        logger.info("invoice_list_requested",
                    requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def retrieve(self, request, *args, pk):
        logger.info("invoice_get_requested",
                    requested_by=request.user.id, role=request.user.role)

        invoice = (self.get_queryset()
                   .select_related('payment')
                   .prefetch_related('line_items')
                   .get(pk=pk)
                   )
        data = InvoiceDetailsSerializer(invoice).data

        logger.info("invoice_detail_loaded",
                    requested_by=request.user.id, role=request.user.role)
        return Response(data, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN, ROLE.COORDINATOR])
    def partial_update(self, request, *args, **kwargs):
        logger.info("invoice_partial_update_requested",
                    requested_by=request.user.id, role=request.user.role)

        # Get the invoice with payment data
        invoice = self.get_queryset().select_related(
            'payment').get(pk=kwargs['pk'])

        # Check if payment exists and is completed
        if hasattr(invoice, 'payment') and invoice.payment:
            if invoice.payment.status == 'completed':
                logger.warning("invoice_partial_update_blocked",
                               requested_by=request.user.id,
                               invoice_id=kwargs['pk'],
                               payment_status=invoice.payment.status,
                               reason="Invoice is closed due to completed payment")
                raise PermissionDenied(
                    detail="This invoice is closed and cannot be updated because the payment has been completed."
                )

        logger.info("invoice_partial_update_allowed",
                    requested_by=request.user.id,
                    invoice_id=kwargs['pk'])

        return super().partial_update(request, *args, **kwargs)


class InvoicePdfView(APIView):

    def get(self, request, pk):
        try:
            # Use select_related for ForeignKey/OneToOne relationships
            invoice = Invoice.objects.select_related(
                'enrollment',  # This is the field name in Invoice model
                'enrollment__student',  # If enrollment has student
                'enrollment__student__user',  # If student has user
                'enrollment__course_offering',  # If enrollment has course
                'payment'  # Also include payment if needed
            ).prefetch_related(
                'line_items'  # Reverse relationship for line items
            ).get(pk=pk)

            # Debug - check if enrollment exists
            print(f"Invoice ID: {invoice.id}")
            print(f"Enrollment exists: {hasattr(invoice, 'enrollment')}")
            if hasattr(invoice, 'enrollment') and invoice.enrollment:
                print(f"Enrollment ID: {invoice.enrollment.id}")
                print(f"Student: {invoice.enrollment.student}")
            else:
                print("No enrollment found for this invoice")

            pdf = InvoicePdfService.generate(invoice)

            response = HttpResponse(
                pdf.getvalue(),
                content_type="application/pdf"
            )

            response[
                "Content-Disposition"
            ] = f'attachment; filename="{invoice.invoice_number}.pdf"'

            return response

        except Invoice.DoesNotExist:
            return Response(
                {"error": "Invoice not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

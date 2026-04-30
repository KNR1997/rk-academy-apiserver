from django.urls import path

from academy.app.views.enrollment.base import EnrollmentViewSet, EnrollmentPendingPaymentViewSet
from academy.app.views.enrollment.payment import EnrollmentPaymentViewSet

urlpatterns = [
    path(
        "enrollments/",
        EnrollmentViewSet.as_view({"get": "list", "post": "create"}),
        name="enrollment",
    ),
    path(
        "enrollments/<uuid:pk>/",
        EnrollmentViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="enrollment",
    ),
    path(
        "enrollment-payments/",
        EnrollmentPaymentViewSet.as_view({"get": "list", "post": "create"}),
        name="enrollment-payment",
    ),
    path(
        "enrollment-payments/<uuid:pk>/",
        EnrollmentPaymentViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="enrollment-payment",
    ),
    path(
        "enrollment-payments/pending-payments",
        EnrollmentPendingPaymentViewSet.as_view({"get": "list"}),
        name="enrollment-payment",
    ),
]

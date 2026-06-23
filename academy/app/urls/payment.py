from django.urls import path

from academy.app.views.payment.base import PaymentCreateAPIEndpoint

urlpatterns = [
    path(
        "payments/",
        PaymentCreateAPIEndpoint.as_view(http_method_names=["post"]),
        name="payment",
    ),
]

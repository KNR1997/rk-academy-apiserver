from django.urls import path

from academy.app.views.subject.base import SubjectViewSet

urlpatterns = [
    path(
        "subjects/",
        SubjectViewSet.as_view({"get": "list", "post": "create"}),
        name="subject",
    ),
    path(
        "subjects/<str:slug>/",
        SubjectViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="subject",
    ),
]

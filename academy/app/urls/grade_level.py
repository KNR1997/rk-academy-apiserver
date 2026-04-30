from django.urls import path

from academy.app.views.grade_level.base import GradeLevelViewSet

urlpatterns = [
    path(
        "grade-levels/",
        GradeLevelViewSet.as_view({"get": "list", "post": "create"}),
        name="gradeLevel",
    ),
    path(
        "grade-levels/<uuid:pk>/",
        GradeLevelViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="gradeLevel",
    ),
]

from django.urls import path

from academy.app.views.academic_year.base import AcademicYearViewSet

urlpatterns = [
    path(
        "academicYears/",
        AcademicYearViewSet.as_view({"get": "list", "post": "create"}),
        name="academicYear",
    ),
    path(
        "academicYears/<uuid:pk>/",
        AcademicYearViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="academicYear",
    ),
]

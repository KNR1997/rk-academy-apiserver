from django.urls import path

from academy.app.views.teacher.base import TeacherViewSet
from academy.app.views.teacher.course_offering import TeacherCourseOfferingViewSet

urlpatterns = [
    path(
        "teachers/",
        TeacherViewSet.as_view({"get": "list", "post": "create"}),
        name="teacher",
    ),
    path(
        "teachers/<uuid:pk>/",
        TeacherViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="teacher",
    ),
    path(
        "teachers/me/course-offerings",
        TeacherCourseOfferingViewSet.as_view({"get": "list"}),
        name="teacher-course-offering",
    ),
    path(
        "teachers/me/course-offerings/<uuid:pk>/",
        TeacherCourseOfferingViewSet.as_view({"get": "retrieve"}),
        name="teacher-course-offering",
    ),
]

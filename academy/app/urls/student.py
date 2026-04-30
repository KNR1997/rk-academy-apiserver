from django.urls import path

from academy.app.views.student.base import StudentViewSet, StudentEnrollmentsEndpoint
# from academy.app.views.student.me import StudentMeEnrollmentViewSet, StudentMeEnrollmentVideosViewSet
# from academy.app.views.student.video import StudentWatchVideoEndpoint

urlpatterns = [
    path(
        "students/",
        StudentViewSet.as_view({"get": "list", "post": "create"}),
        name="student",
    ),
    path(
        "students/<uuid:pk>/",
        StudentViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="student",
    ),
    path(
        "students/<uuid:pk>/enrollments",
        StudentEnrollmentsEndpoint.as_view(),
        name="student-enrollments",
    ),

    # path(
    #     "students/me/enrollments/",
    #     StudentMeEnrollmentViewSet.as_view({"get": "list"}),
    #     name="student-me-enrollments",
    # ),
    # path(
    #     "students/me/enrollments/<uuid:pk>/videos",
    #     StudentMeEnrollmentVideosViewSet.as_view({"get": "list"}),
    #     name="student-me-enrollment-videos",
    # ),
    # path(
    #     "students/me/watch-videos/<uuid:pk>/",
    #     StudentWatchVideoEndpoint.as_view(),
    #     name="student-me-watch-video",
    # ),
]

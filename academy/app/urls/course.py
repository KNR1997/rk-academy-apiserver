from django.urls import path

from academy.app.views.course.base import CourseViewSet
from academy.app.views.course_offering.base import CourseOfferingViewSet
from academy.app.views.course_offering.enrollment import CourseOfferingEnrollmentViewSet

urlpatterns = [
    path(
        "courses/",
        CourseViewSet.as_view({"get": "list", "post": "create"}),
        name="course",
    ),
    path(
        "courses/<str:slug>/",
        CourseViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="course",
    ),
    path(
        "course-offerings/",
        CourseOfferingViewSet.as_view({"get": "list", "post": "create"}),
        name="course-offering",
    ),
    path(
        "course-offerings/<uuid:pk>/",
        CourseOfferingViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="course-offering",
    ),
    path(
        "course-offerings/<uuid:course_offering_id>/enrollments/",
        CourseOfferingEnrollmentViewSet.as_view({
            "get": "list",
        }),
        name="course-offering-enrollment",
    ),

    # path(
    #     "course-contents/",
    #     CourseContentListCreateAPIEndpoint.as_view({"get": "list", "post": "create"}),
    #     name="course-content",
    # ),
    # path(
    #     "course-contents/<uuid:pk>/",
    #     CourseContentDetailAPIEndpoint.as_view(http_method_names=[
    #         "get",
    #         "patch",
    #         "delete"
    #     ]),
    #     name="course-content",
    # ),
]

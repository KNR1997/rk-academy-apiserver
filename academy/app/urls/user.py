from django.urls import path

from academy.app.views.user.admin import AdminViewSet, ResetTeacherPasswordEndpoint
from academy.app.views.user.base import UserViewSet
from academy.app.views.user.coordinator import CoordinatorViewSet

urlpatterns = [
    path(
        "users/",
        UserViewSet.as_view({"get": "list", "post": "create"}),
        name="user",
    ),
    path(
        "users/<uuid:pk>/",
        UserViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="user",
    ),
    path(
        "users/block-user",
        UserViewSet.as_view({"post": "deactivate"}),
        name="user",
    ),

    path(
        "admin/list/",
        AdminViewSet.as_view({"get": "list", "post": "create"}),
        name="admin",
    ),
    path(
        "admin/teacher/<uuid:teacher_id>/reset-password",
        ResetTeacherPasswordEndpoint.as_view(),
        name="reset-teacher-password",
    ),

    path(
        "coordinators/",
        CoordinatorViewSet.as_view({"get": "list", "post": "create"}),
        name="coordinator",
    ),
    path(
        "coordinators/<uuid:pk>/",
        CoordinatorViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="coordinator",
    ),
]

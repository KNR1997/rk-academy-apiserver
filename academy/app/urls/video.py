from django.urls import path

from academy.app.views.video.base import VideoListCreateAPIEndpoint, VideoDetailAPIEndpoint

urlpatterns = [
    path(
        "videos/",
        VideoListCreateAPIEndpoint.as_view({"get": "list", "post": "create"}),
        name="video",
    ),
    path(
        "videos/<uuid:pk>/",
        VideoDetailAPIEndpoint.as_view(http_method_names=["get", "patch", "delete"]),
        name="video",
    ),
]

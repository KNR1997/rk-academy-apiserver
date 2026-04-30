from django.urls import path

from academy.app.views.conversation.base import ConversationViewSet

urlpatterns = [
    path(
        "conversations/",
        ConversationViewSet.as_view({"get": "list", "post": "create"}),
        name="conversation",
    ),
    path(
        "conversations/<uuid:pk>/",
        ConversationViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="conversation",
    ),
]

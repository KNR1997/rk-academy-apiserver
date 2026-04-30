from django.urls import path

from academy.app.views.message.base import MessageViewSet
from academy.app.views.message.conversation import ConversationMessagesViewSet

urlpatterns = [
    path(
        "messages/",
        MessageViewSet.as_view({"get": "list", "post": "create"}),
        name="message",
    ),
    path(
        "messages/conversations/<uuid:pk>/",
        ConversationMessagesViewSet.as_view({
            "get": "list",
            "post": "create",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="message",
    ),
]

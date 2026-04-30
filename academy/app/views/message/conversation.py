from rest_framework import status
from rest_framework.response import Response

from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.message import MessageListSerializer, MessageSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Message


# Create your views here.
class ConversationMessagesViewSet(BaseViewSet):
    model = Message
    serializer_class = MessageListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(conversation_id=self.kwargs["pk"])
            .select_related("sender")
            .order_by("created_at")
        )

    @allow_permission([ROLE.ADMIN])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN, ROLE.TEACHER])
    def create(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

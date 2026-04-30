from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.message import MessageListSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Message, Message


# Create your views here.
class MessageViewSet(BaseViewSet):
    model = Message
    serializer_class = MessageListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

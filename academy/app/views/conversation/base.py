# Third party imports
import structlog
from crum import get_current_user
from rest_framework import status
from rest_framework.response import Response

# Module imports
from academy.app.permissions.base import allow_permission, ROLE
from academy.app.serializers.conversation import ConversationListSerializer, ConversationSerializer
from academy.app.views.base import BaseViewSet
from academy.db.models import Conversation

logger = structlog.getLogger(__name__)


# Create your views here.
class ConversationViewSet(BaseViewSet):
    model = Conversation
    serializer_class = ConversationListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        current_user = get_current_user()

        queryset = (
            self.filter_queryset(
                super()
                .get_queryset()
                .filter(participants__user=current_user)
                # .select_related("latest_message")
                .prefetch_related("participants__user")
                .distinct()
            )
        )
        logger.info("conversation_queryset_loaded", user_id=self.request.user.id, role=self.request.user.role)
        return queryset

    def list(self, request, *args, **kwargs):
        logger.info("conversation_list_requested", requested_by=request.user.id, role=request.user.role)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("conversation_get_requested", conversation_id=self.kwargs.get('pk'), requested_by=request.user.id,
                    role=request.user.role)
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        logger.info("conversation_create_started", requested_by=request.user.id)

        serializer = ConversationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation = serializer.save()

        logger.info("conversation_created", conversation_id=conversation.id, created_by=request.user.id)
        return Response(None, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        logger.info("conversation_update_requested", conversation_id=self.kwargs.get('pk'),
                    requested_by=request.user.id,
                    role=request.user.role)
        return super().update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        logger.info("conversation_partial_update_requested", conversation_id=self.kwargs.get('pk'),
                    requested_by=request.user.id,
                    role=request.user.role)
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        logger.info("conversation_destroy_requested", conversation_id=self.kwargs.get('pk'),
                    requested_by=request.user.id,
                    role=request.user.role)
        return super().destroy(request, *args, **kwargs)

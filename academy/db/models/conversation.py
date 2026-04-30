import uuid

from django.db import models

from academy.db.mixins import TimeAuditModel


class Conversation(TimeAuditModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    latest_message = models.ForeignKey(
        "db.Message",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    is_group = models.BooleanField(default=False)

    class Meta:
        db_table = "conversation"


class ConversationParticipant(TimeAuditModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    conversation = models.ForeignKey(
        "db.Conversation",
        related_name="participants",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        "db.User",
        related_name="conversation_participations",
        on_delete=models.CASCADE
    )

    last_read_message = models.ForeignKey(
        "db.Message",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = ("conversation", "user")

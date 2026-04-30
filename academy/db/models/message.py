import uuid

from django.db import models

from academy.db.mixins import TimeAuditModel


class Message(TimeAuditModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    conversation = models.ForeignKey(
        "Conversation",
        related_name="messages",
        on_delete=models.CASCADE
    )

    sender = models.ForeignKey(
        "db.User",
        related_name="sent_messages",
        on_delete=models.CASCADE
    )

    body = models.TextField()

    is_edited = models.BooleanField(default=False)

    class Meta:
        db_table = "message"
        ordering = ["created_at"]

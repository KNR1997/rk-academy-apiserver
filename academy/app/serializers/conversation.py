from crum import get_current_user
from django.db import transaction
from rest_framework import serializers

from academy.app.serializers.base import BaseSerializer
from academy.app.serializers.user import UserLiteSerializer
from academy.db.models import Conversation, User
from academy.db.models.conversation import ConversationParticipant


class ConversationParticipantListSerializer(BaseSerializer):
    user = UserLiteSerializer()

    class Meta:
        model = ConversationParticipant
        fields = (
            'id',
            'user',
        )


class ConversationListSerializer(BaseSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            'id',
            'latest_message',
            'is_group',
            'created_at',
            'participants',
        )

    def get_participants(self, obj):
        current_user = get_current_user()

        participants = obj.participants.exclude(
            user_id=current_user.id
        )

        return ConversationParticipantListSerializer(
            participants,
            many=True
        ).data


class ConversationSerializer(BaseSerializer):
    participant_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "participant_id", "created_at"]

    def validate_participant_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            participant_id = validated_data.pop("participant_id")
            current_user = get_current_user()

            if participant_id == current_user.id:
                raise serializers.ValidationError(
                    "Cannot create conversation with yourself"
                )

            existing = Conversation.objects.filter(
                participants__user=current_user
            ).filter(
                participants__user_id=participant_id
            ).distinct()

            if existing.exists():
                return existing.first()

            conversation = Conversation.objects.create(**validated_data)

            ConversationParticipant.objects.bulk_create([
                ConversationParticipant(
                    conversation=conversation,
                    user=current_user
                ),
                ConversationParticipant(
                    conversation=conversation,
                    user_id=participant_id
                )
            ])

            return conversation

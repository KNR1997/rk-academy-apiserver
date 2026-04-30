from crum import get_current_user
from rest_framework import serializers

from academy.app.serializers.base import BaseSerializer
from academy.app.serializers.user import UserLiteSerializer
from academy.db.models import Message


class MessageListSerializer(BaseSerializer):
    sender = UserLiteSerializer()
    my_message = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = '__all__'

    def get_my_message(self, obj):
        current_user = get_current_user()
        return obj.sender_id == current_user.id


class MessageSerializer(BaseSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender']

    def create(self, validated_data):
        current_user = get_current_user()

        validated_data['sender_id'] = current_user.id

        return super().create(validated_data)

from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'channel', 'status', 'sent_at']
        read_only_fields = ['id', 'sent_at']
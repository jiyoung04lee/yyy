from rest_framework import serializers
from .models import Notice

class NoticeSerializer(serializers.ModelSerializer):
    notice_type_display = serializers.CharField(source="get_notice_type_display", read_only=True)

    class Meta:
        model = Notice
        fields = ["id", "notice_type", "notice_type_display", "message", "is_read", "created_at"]
        read_only_fields = ["id", "created_at", "notice_type_display", "message"]
        
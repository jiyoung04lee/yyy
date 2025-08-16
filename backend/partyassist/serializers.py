from rest_framework import serializers
from detailview.models import Party
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "profile_image"]  # User 모델에 profile_image 필드 있다고 가정

class MyPartySerializer(serializers.ModelSerializer):
    # 참여자 프로필 (일부만)
    participants = serializers.SerializerMethodField()
    participation_count = serializers.SerializerMethodField()

    class Meta:
        model = Party
        fields = [
            "id",
            "title",
            "location_name",
            "image",
            "start_time",
            "capacity",
            "participation_count",
            "participants",
        ]

    def get_participation_count(self, obj):
        return obj.participations.count()

    def get_participants(self, obj):
        qs = obj.participations.select_related("user")[:5]  # 최대 5명만
        return UserProfileSerializer([p.user for p in qs], many=True).data
    
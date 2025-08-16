from rest_framework import serializers
from detailview.models import Party, Participation
from mypage.models import ExtraSetting
from django.contrib.auth import get_user_model

User = get_user_model()

class ExtraSettingSerializer(serializers.ModelSerializer):
    mbti = serializers.SerializerMethodField()

    class Meta:
        model = ExtraSetting
        fields = ["grade", "college", "personality", "mbti"]

    def get_mbti(self, obj):
        # 네 필드 합쳐서 "ENFP" 같은 문자열로 반환
        return f"{obj.mbti_i_e}{obj.mbti_n_s}{obj.mbti_f_t}{obj.mbti_p_j}".upper()

class UserProfileSerializer(serializers.ModelSerializer):
    extra_setting = ExtraSettingSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "profile_image",
            "intro",
            "extra_setting"  # 추가 설정 정보 포함
        ]

class PartyParticipantSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Participation
        fields = ["id", "user", "is_standby"]
        
        

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
    
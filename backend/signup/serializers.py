from django.conf import settings
from rest_framework import serializers

class KakaoLoginRequestSerializer(serializers.Serializer):
    code = serializers.CharField()
    redirect_uri = serializers.URLField()

    def validate_redirect_uri(self, value):
        #화이트리스트로 리다이렉트 URI 검증
        allowed = getattr(settings, "KAKAO_ALLOWED_REDIRECT_URIS", [])
        if allowed and value not in allowed:
            raise serializers.ValidationError("redirect_uri mismatch")
        return value

class UserBriefSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField(allow_blank=True, allow_null=True, required=False)
    nickname = serializers.CharField(allow_blank=True, required=False)

class TokenPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserBriefSerializer()

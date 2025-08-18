from django.conf import settings
from rest_framework import serializers
import re
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="이미 사용 중인 이메일입니다.")]
    )
    phone = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="이미 사용 중인 전화번호입니다.")]
    )

    class Meta:
        model = User
        fields = ["username", "password", "email", "phone"]

    def validate_phone(self, value):
        value = value.strip()
        if not re.match(r"^\d+$", value):
            raise serializers.ValidationError("전화번호는 숫자만 입력해야 합니다. (하이픈 '-' 제외)")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            phone=validated_data["phone"],
        )
        return user
    

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

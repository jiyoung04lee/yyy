import re
from rest_framework import serializers
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
        value = value.strip()  # 공백 제거
        if not re.match(r"^\d+$", value):
            raise serializers.ValidationError("전화번호는 숫자만 입력해야 합니다. (하이픈 '-' 제외)")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            phone=validated_data["phone"]
        )
        return user

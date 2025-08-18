from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    # 닉네임 (선택)
    nickname = models.CharField(max_length=30, blank=True)

    # 이메일 & 전화번호 → 회원가입 시 필수
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)

    # 프로필 관련
    intro = models.CharField("한줄소개", max_length=255, blank=True, null=True)
    profile_image = models.ImageField("프로필 사진", upload_to="profiles/", blank=True, null=True)

    # 유저 활동 관련
    points = models.PositiveIntegerField("포인트", default=0)         # 포인트 잔액
    warnings = models.PositiveIntegerField("경고 횟수", default=0)    # 누적 경고 횟수

    def __str__(self):
        return self.username or f"user-{self.pk}"


class SocialAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20, default="kakao")
    social_id = models.CharField(max_length=255, unique=True, db_index=True)

    class Meta:
        unique_together = ("provider", "social_id")

    def __str__(self):
        return f"{self.provider}:{self.social_id} -> {self.user_id}"

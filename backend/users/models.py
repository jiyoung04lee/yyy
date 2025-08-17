from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True)
    points = models.PositiveIntegerField("포인트", default=0) # 유저의 포인트 잔액 (예약금으로 사용)

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
    
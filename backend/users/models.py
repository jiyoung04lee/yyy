from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 기본 필드(username, password, email, first_name, last_name 등)는 AbstractUser에 포함됨
    name = models.CharField(max_length=50, default="")
    email = models.EmailField(unique=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, blank=True)
    school = models.CharField(max_length=30, default="")

    points = models.PositiveIntegerField(default=0)
    participate_count = models.PositiveIntegerField(default=0)
    warning_count = models.PositiveIntegerField(default=0)

    bio = models.CharField(max_length=120, blank=True, default="")
    profile_image = models.URLField(blank=True, default="")

    # 추가 정보(학년/단과대/MBTI 등)는 JSON으로
    profile_extra = models.JSONField(blank=True, default=dict)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

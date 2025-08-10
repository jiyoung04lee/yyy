from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
     nickname = models.CharField(max_length=30, blank=True)

class SocialAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20, default="kakao")
    social_id = models.CharField(max_length=255, unique=True, db_index=True)

    class Meta:
        unique_together = ("provider", "social_id")

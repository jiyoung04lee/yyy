from django.db import models
from django.utils import timezone
from django.conf import settings

class Place(models.Model):
    # PK(id)는 자동 생성
    name = models.CharField(max_length=120) # 장소 이름 (필수)
    address = models.CharField(max_length=200, default="") # 주소 (빈문자 허용, NULL 금지)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0) # 위도
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)  # 경도
    capacity = models.PositiveIntegerField(default=1) # 수용 가능 인원 (1 이상)
    photo = models.ImageField(upload_to="places/", default="places/default.jpg") # 기본 이미지로 NULL 방지

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Party(models.Model):
    place = models.ForeignKey("detailview.Place", on_delete=models.PROTECT, related_name="parties")
    title = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField(default=timezone.now)
    summary = models.TextField(default="")

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="joined_parties",
        blank=True,  # 비어있을 수는 있지만 NULL은 개념상 없음
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
        check=models.Q(created_at__lte=models.F("start_at")),
        name="party_time_order",
    ),
        ]

    def __str__(self):
        return f"{self.title} @ {self.place.name}"

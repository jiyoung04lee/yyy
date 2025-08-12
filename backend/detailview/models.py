from django.db import models
from django.conf import settings

class Place(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50, default="", blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    capacity = models.PositiveIntegerField(default=1)
    photo = models.ImageField(upload_to="places/", default="places/default_party.jpg")

    def __str__(self): return self.name


class Party(models.Model):
    place = models.ForeignKey(Place, on_delete=models.PROTECT, related_name="parties")
    title = models.CharField(max_length=50)
    max_participants = models.PositiveIntegerField(default=4)
    start_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True) # created_at을 기준으로 start_time이 더 이후여야 함

    def __str__(self): return f"{self.title} @ {self.place.name}"


class Participation(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="participations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="party_participations")

    class Meta:
        unique_together = ("party", "user")  # 중복 신청 방지
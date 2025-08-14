from django.db import models
from django.conf import settings

class Review(models.Model):
    party = models.ForeignKey('detailview.Party', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    q1_rating = models.PositiveSmallIntegerField()
    q2_rating = models.PositiveSmallIntegerField()
    q3_rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('party', 'user')  # 한 유저당 한 파티 리뷰 1개만

    def __str__(self):
        return f"{self.user.username} - {self.party.title} 리뷰"
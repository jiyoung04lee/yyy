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


REPORT_CATEGORIES = [
    ('FAKE_INFO', '개인정보 허위 기재'),
    ('UNPLEASANT', '파티 현장에서의 불쾌감 형성'),
    ('INAPPROPRIATE_ACT', '파티 현장에서의 부적절한 행위'),
    ('BAD_PHOTO', '부적절한 프로필 사진'),
    ('OTHER', '기타'),
]

class Report(models.Model):
    party = models.ForeignKey('detailview.Party', on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_made')
    reported_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_received')
    category = models.CharField(max_length=30, choices=REPORT_CATEGORIES)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # 신고에 대한 대응은 순차적으로 진행해야할 것 같아, 시간 추가

    class Meta:
        unique_together = ('party', 'reporter', 'reported_user')  # 동일 파티 내 동일 대상 중복 신고 방지
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reporter.username} -> {self.reported_user.username} ({self.category})"
    
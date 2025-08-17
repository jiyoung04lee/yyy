from django.db import models
from django.conf import settings

class Payment(models.Model):
    class Status(models.TextChoices):
        SUCCESS = "SUCCESS", "결제 성공"
        FAILED = "FAILED", "결제 실패"
        REFUNDED = "REFUNDED", "환불 완료"

    participation = models.OneToOneField(
        "detailview.Participation", 
        on_delete=models.PROTECT,  # 결제 기록은 참여 정보가 삭제되어도 유지
        related_name="payment"
    )
    user = models.ForeignKey( #유저와 별개로 기록 유지
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name="payments"
    )
    amount = models.PositiveIntegerField("결제 금액")
    status = models.CharField("상태", max_length=20, choices=Status.choices)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}의 {self.amount}원 결제 ({self.status})"
    
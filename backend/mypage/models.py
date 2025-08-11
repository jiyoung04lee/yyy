from django.db import models
from django.conf import settings

class Review(models.Model):
    # FK: 어떤 파티에 대한 리뷰인지
    party = models.ForeignKey(
        "detailview.Party",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    # FK: 리뷰(신고) 작성 유저
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    # 별점 (1~5)
    stars = models.PositiveSmallIntegerField(default=0)

    # 신고/리뷰 내용
    content = models.TextField(default="")

    class Meta:
        # 한 유저가 같은 파티에 리뷰를 중복 작성 못 하도록
        constraints = [
            models.UniqueConstraint(fields=["party", "user"], name="uniq_review_party_user"),
            models.CheckConstraint(check=models.Q(stars__gte=1) & models.Q(stars__lte=5),
                                   name="review_stars_between_1_5"),
        ]
        indexes = [
            models.Index(fields=["party"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"Review(party={self.party_id}, user={self.user_id}, stars={self.stars})"
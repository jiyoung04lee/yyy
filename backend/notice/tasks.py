from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
from detailview.models import Party, Participation
from .models import Notice

# 1. 파티 오픈 1일 전 알림
@shared_task
def create_party_open_notices():
    now = timezone.now()
    target_start = now + timedelta(days=1)
    target_end = target_start + timedelta(hours=1)  # ±1시간 범위

    parties = Party.objects.filter(
        start_time__range=(target_start, target_end),
        current_participants=F("max_participants")  # 정원 꽉 찬 경우
    )

    for party in parties:
        participants = Participation.objects.filter(party=party)
        for p in participants:
            Notice.objects.create(
                user=p.user,
                notice_type=Notice.PARTY_OPEN_1DAY,
                message=f"신청하신 '{party.title}'가 곧 열릴 예정이에요. 파티 즐길 준비 됐나요?"
            )


# 2. 파티 인원 미달로 취소 알림 (오픈 1일 전인데 정원 미달)
@shared_task
def create_insufficient_party_notices():
    now = timezone.now()
    target_start = now + timedelta(days=1)
    target_end = target_start + timedelta(hours=1)

    parties = Party.objects.filter(
        start_time__range=(target_start, target_end),
        current_participants__lt=F("min_participants")  # 최소인원 미달
    )

    for party in parties:
        participants = Participation.objects.filter(party=party)
        for p in participants:
            Notice.objects.create(
                user=p.user,
                notice_type=Notice.PARTY_INSUFFICIENT,
                message=f"신청하신 '{party.title}'이(가) 신청 인원 미달로 취소됐어요. 다음에 더 재밌는 자리로 찾아올게요."
            )


# 3. 새 파티 생성 알림
@shared_task
def create_new_party_notice(party_id):
    try:
        party = Party.objects.get(id=party_id)
    except Party.DoesNotExist:
        return

    # 예: 전체 유저한테 알림 보내기 (실제로는 팔로워나 관심사 맞는 유저만)
    from django.contrib.auth import get_user_model
    User = get_user_model()

    for user in User.objects.exclude(id=party.host.id):  # 파티 주최자 제외
        Notice.objects.create(
            user=user,
            notice_type=Notice.PARTY_NEW,
            message=f"새로운 파티가 열렸어요! '{party.title}'에서 새로운 친구들을 만나보세요."
        )

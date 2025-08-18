from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from detailview.models import Participation, Party
from .models import Payment

class JoinAndReserveSerializer(serializers.Serializer):
    party_id = serializers.IntegerField()

    def validate_party_id(self, value):
        try:
            party = Party.objects.get(id=value)
        except Party.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 파티입니다.")
        return party

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        party = validated_data["party_id"]

        # 정원 확인
        confirmed_count = party.participations.filter(status=Participation.Status.CONFIRMED).count()
        if confirmed_count >= party.max_participants:
            raise serializers.ValidationError("정원이 가득 찼습니다.")

        # 기존 참여 여부 확인
        existing = Participation.objects.filter(user=user, party=party).first()
        if existing:
            # 내가 만든 Participation이 이미 있는데
            # 결제 대기 상태라면 → 결제 처리
            if existing.status == Participation.Status.PENDING_PAYMENT:
                participation = existing
            else:
                raise serializers.ValidationError(f"이미 신청한 파티입니다. 현재 상태: {existing.get_status_display()}")
        else:
            # Participation 신규 생성 (결제 대기)
            participation = Participation.objects.create(
                user=user,
                party=party,
                status=Participation.Status.PENDING_PAYMENT
            )

        # 본인 확인 (예방 차원, 혹시라도 타인의 Participation id를 쓸 경우)
        if participation.user != user:
            raise serializers.ValidationError("본인의 예약만 결제할 수 있습니다.")

        # 상태 확인
        if participation.status != Participation.Status.PENDING_PAYMENT:
            raise serializers.ValidationError(
                f"결제 대기 상태가 아닙니다. 현재 상태: {participation.get_status_display()}"
            )

        # 포인트 확인
        if user.points < party.deposit:
            raise serializers.ValidationError(
                f"포인트가 부족합니다. 필요한 포인트: {party.deposit}, 보유 포인트: {user.points}"
            )

        # 포인트 차감 + 확정
        user.points -= party.deposit
        user.save(update_fields=["points"])
        participation.status = Participation.Status.CONFIRMED
        participation.paid_at = timezone.now()
        participation.save(update_fields=["status", "paid_at"])

        # 결제 기록 생성
        payment = Payment.objects.create(
            user=user,
            participation=participation,
            amount=party.deposit,
            status=Payment.Status.SUCCESS
        )

        return payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "participation", "user", "amount", "status", "created_at"]
        read_only_fields = fields
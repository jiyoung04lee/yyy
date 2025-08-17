from django.db import transaction
from rest_framework import serializers
from .models import Payment
from users.models import User
from detailview.models import Participation

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "participation", "user", "amount", "status", "created_at"]
        read_only_fields = fields

class CreatePaymentSerializer(serializers.Serializer):
    participation_id = serializers.IntegerField()

    def validate(self, attrs):
        participation_id = attrs["participation_id"]
        request = self.context["request"]
        user = request.user

        try:
            participation = Participation.objects.select_related("party").get(id=participation_id)
        except Participation.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 예약 정보입니다.")

        # 검증 로직
        if participation.user != user:
            raise serializers.ValidationError("본인의 예약만 결제할 수 있습니다.")
        if participation.status != Participation.Status.PENDING_PAYMENT:
            raise serializers.ValidationError(f"결제 대기 상태가 아닙니다. 현재 상태: {participation.get_status_display()}")
        
        party = participation.party
        if user.points < party.deposit:
            raise serializers.ValidationError(f"포인트가 부족합니다. 필요한 포인트: {party.deposit}, 보유 포인트: {user.points}")

        attrs["user"] = user
        attrs["participation"] = participation
        attrs["party"] = party
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data["user"]
        party = validated_data["party"]
        participation = validated_data["participation"]

        # 1. 유저 포인트 차감
        user.points -= party.deposit
        user.save(update_fields=["points"])

        # 2. 참여 상태 변경
        participation.status = Participation.Status.CONFIRMED
        participation.save(update_fields=["status"])

        # 3. 결제 기록 생성
        payment = Payment.objects.create(
            user=user,
            participation=participation,
            amount=party.deposit,
            status=Payment.Status.SUCCESS
        )
        return payment

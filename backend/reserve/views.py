from rest_framework import generics, permissions
from .serializers import CreatePaymentSerializer, PaymentSerializer

class CreatePaymentView(generics.CreateAPIView):
    """
    예약금 결제를 처리하는 API
    POST /api/reserve/pay/
    Body: { "participation_id": 123 }
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreatePaymentSerializer

    def get_serializer_context(self):
        # 시리얼라이저에 request 객체를 넘겨주어 유저 정보에 접근할 수 있게 함
        return {"request": self.request, **super().get_serializer_context()}

    def get_queryset(self):
        # 이 뷰는 생성(Create)만 담당하므로 queryset이 필요 없긴함 (형식상으로 남겨둠)
        # 현재 사용자와 관련된 queryset을 반환하도록 설정
        return self.request.user.payments.none()
    
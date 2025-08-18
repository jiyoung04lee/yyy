from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import JoinAndReserveSerializer, PaymentSerializer

class JoinAndReserveView(generics.CreateAPIView):
    """
    참가 신청 + 결제를 동시에 처리하는 API
    POST /api/reserve/join/
    Body: { "party_id": 1 }
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JoinAndReserveSerializer

    def get_serializer_context(self):
        return {"request": self.request, **super().get_serializer_context()}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        return Response(PaymentSerializer(payment).data)
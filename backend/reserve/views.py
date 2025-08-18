from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import JoinAndReserveSerializer, PaymentSerializer

class JoinAndReserveView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JoinAndReserveSerializer

    def get_serializer_context(self):
        return {"request": self.request, **super().get_serializer_context()}

    def create(self, request, *args, **kwargs):
        # URL 경로에서 party_id 꺼내기
        party_id = self.kwargs.get("party_id")
        serializer = self.get_serializer(data={"party_id": party_id})
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        return Response(PaymentSerializer(payment).data)
    

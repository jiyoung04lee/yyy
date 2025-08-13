from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Count
from .models import Party, Participation
from .serializers import PartyListSerializer, PartyDetailSerializer


class PartyViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = [AllowAny]

    def get_queryset(self): # 파티 목록 조회 가능
        return (
            Party.objects
            .select_related("place")
            .prefetch_related("tags", "participations__user")
            .annotate(applied_count=Count("participations"))
            .order_by("start_time")
        )

    def get_serializer_class(self): # 파티 상세 정보 조회 가능
        if self.action == "retrieve":
            return PartyDetailSerializer
        return PartyListSerializer


class PartyJoinAPIView(APIView): # 파티 참가 신청

    permission_classes = [IsAuthenticated]

    def post(self, request, party_id):
        try:
            party = Party.objects.get(pk=party_id)
        except Party.DoesNotExist:
            return Response({"detail": "파티가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 중복 신청 방지
        if Participation.objects.filter(party=party, user=request.user).exists():
            return Response({"detail": "이미 신청한 파티입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 정원 초과 방지
        if party.participations.count() >= party.max_participants:
            return Response({"detail": "정원이 초과되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 참가 신청 생성
        Participation.objects.create(party=party, user=request.user)
        return Response({"detail": "파티 신청 완료!"}, status=status.HTTP_201_CREATED)
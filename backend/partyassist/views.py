from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from detailview.models import Participation
from .permissions import IsPartyParticipant
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class StandbyViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated & IsPartyParticipant]

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        participation = Participation.objects.get(party_id=pk, user=request.user)

        # toggle
        participation.is_standby = not participation.is_standby
        participation.save()

        # 카운트 계산
        participation_count = Participation.objects.filter(party_id=pk).count()
        standby_count = Participation.objects.filter(party_id=pk, is_standby=True).count()

        # WebSocket 브로드캐스트
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"party_{pk}",
            {
                "type": "send_standby_update",
                "data": {
                    "party_id": pk,
                    "participation_count": participation_count,
                    "standby_count": standby_count
                }
            }
        )

        return Response({
            "party_id": pk,
            "user_id": request.user.id,
            "is_standby": participation.is_standby,
            "participation_count": participation_count,
            "standby_count": standby_count
        }, status=status.HTTP_200_OK)
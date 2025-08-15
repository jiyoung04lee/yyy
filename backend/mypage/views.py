from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Review, Report, ExtraSetting
from .serializers import ReviewSerializer, ReportSerializer, ExtraSettingFromJsonSerializer
from .permissions import IsParticipantOrAdmin, IsOwner

# 리뷰
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsParticipantOrAdmin]

# 신고
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsParticipantOrAdmin]

# 프로필 추가 설정
class ExtraSettingViewSet(viewsets.ModelViewSet):
    queryset = ExtraSetting.objects.all()
    serializer_class = ExtraSettingFromJsonSerializer
    permission_classes = [IsAuthenticated, IsOwner]

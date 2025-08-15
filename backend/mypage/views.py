from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Review, Report, ExtraSetting
from .serializers import ReviewSerializer, ReportSerializer, ExtraSettingFromJsonSerializer
from .permissions import IsParticipantOrAdmin, IsOwner


# -------------------------
# 공통 베이스 뷰: 생성만 가능
# -------------------------
class CreateOnlyViewSet(viewsets.ModelViewSet):
    """
    POST만 허용, 나머지 메서드는 전부 차단
    (목록 조회, 상세 조회, 수정, 삭제 불가)
    """
    def list(self, request, *args, **kwargs):
        self.permission_denied(request, message="목록 조회는 허용되지 않습니다.")

    def retrieve(self, request, *args, **kwargs):
        self.permission_denied(request, message="상세 조회는 허용되지 않습니다.")

    def update(self, request, *args, **kwargs):
        self.permission_denied(request, message="수정은 허용되지 않습니다.")

    def partial_update(self, request, *args, **kwargs):
        self.permission_denied(request, message="수정은 허용되지 않습니다.")

    def destroy(self, request, *args, **kwargs):
        self.permission_denied(request, message="삭제는 허용되지 않습니다.")


# -------------------------
# 리뷰
# -------------------------
class ReviewViewSet(CreateOnlyViewSet):
    """
    - 생성: 로그인 + 해당 파티 참여자만 가능 (IsParticipantOrAdmin)
    - 검증: 참여 여부, 중복 작성 방지 → ReviewSerializer에서 처리
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsParticipantOrAdmin]


# -------------------------
# 신고
# -------------------------
class ReportViewSet(CreateOnlyViewSet):
    """
    - 생성: 로그인 + 해당 파티 참여자만 가능 (IsParticipantOrAdmin)
    - 검증: 참여 여부, 자기 자신 신고 방지, 중복 신고 방지 → ReportSerializer에서 처리
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsParticipantOrAdmin]


# -------------------------
# 프로필 추가 설정
# -------------------------
class ExtraSettingViewSet(viewsets.ModelViewSet):
    """
    - 생성: 본인만 가능, 이미 있으면 생성 불가
    - 조회/수정/삭제: 본인만 가능
    - 데이터 포맷: ExtraSettingFromJsonSerializer (JSON 덩어리 파싱)
    - 추가: /me/ 엔드포인트로 본인 데이터 바로 조회 가능
    """
    queryset = ExtraSetting.objects.all()
    serializer_class = ExtraSettingFromJsonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        # 중복 생성 방지
        if ExtraSetting.objects.filter(user=request.user).exists():
            return Response(
                {"detail": "이미 추가 설정이 존재합니다. 수정 기능을 이용하세요."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        현재 로그인한 사용자의 ExtraSetting 데이터 반환
        """
        try:
            setting = ExtraSetting.objects.get(user=request.user)
            serializer = self.get_serializer(setting)
            return Response(serializer.data)
        except ExtraSetting.DoesNotExist:
            return Response({"detail": "추가 설정이 존재하지 않습니다."}, status=404)

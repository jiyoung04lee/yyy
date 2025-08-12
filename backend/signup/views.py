import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import SocialAccount

from signup.serializers import (
    KakaoLoginRequestSerializer,
    TokenPairResponseSerializer,
    UserBriefSerializer,
)

User = get_user_model()

#테스트용 뷰        
from django.http import HttpResponse

def kakao_callback_debug(request):
    code = request.GET.get("code", "")
    error = request.GET.get("error", "")
    return HttpResponse(f"code={code}<br>error={error}")


class KakaoLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not settings.ENABLE_AUTH:
            # 인증 비활성화 모드 → 그냥 더미 토큰과 유저 반환
            user = User.objects.first()  # 첫 번째 유저를 가짜 로그인으로 사용
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            return Response({
                "access": str(access),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "nickname": getattr(user, "nickname", ""),
                }
            }, status=200)
        
        in_ser = KakaoLoginRequestSerializer(data=request.data)
        in_ser.is_valid(raise_exception=True)
        code = in_ser.validated_data["code"]
        redirect_uri = in_ser.validated_data["redirect_uri"]

        # 1) code -> access_token
        token_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_REST_API_KEY,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        if getattr(settings, "KAKAO_CLIENT_SECRET", ""):
            data["client_secret"] = settings.KAKAO_CLIENT_SECRET

        try:
            t = requests.post(
                token_url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
                timeout=7,
            )
            t.raise_for_status()
            access_token = t.json().get("access_token")
            if not access_token:
                return Response({"detail": "no access_token", "raw": t.text}, status=502)
        except requests.RequestException as e:
            return Response({"detail": f"Kakao token error: {e}"}, status=502)

        # 2) access_token -> profile
        try:
            me = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=7,
            )
            me.raise_for_status()
            payload = me.json()
        except requests.RequestException as e:
            return Response({"detail": f"Kakao userinfo error: {e}"}, status=502)

        kakao_id = payload.get("id")
        account = (payload.get("kakao_account") or {})
        profile = (account.get("profile") or {})
        email = account.get("email")  # 동의 안 하면 None
        nickname = profile.get("nickname") or f"kakao_{kakao_id}"

        if not kakao_id:
            return Response({"detail": "invalid kakao payload"}, status=400)

        # 3) upsert user + social account
        try:
            with transaction.atomic():
                user = None
                if email:
                    user = User.objects.filter(email=email).first()
                if not user:
                    user = User.objects.create_user(
                        username=f"kakao_{kakao_id}",
                        email=email or "",
                        password=None,
                    )
                    # 권장: 소셜 전용 계정 명시
                    user.set_unusable_password()
                    user.save(update_fields=["password"])

                    if hasattr(user, "nickname") and nickname:
                        user.nickname = nickname
                        user.save(update_fields=["nickname"])

                SocialAccount.objects.get_or_create(
                    user=user, provider="kakao", social_id=str(kakao_id)
                )
        except Exception as e:
            return Response({"detail": f"user upsert error: {e}"}, status=500)

        # 4) issue JWT
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # 응답을 시리얼라이저로 감싸서 스키마 고정
        out = {
            "access": str(access),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "nickname": getattr(user, "nickname", nickname),
                # 필요하면 아래 두 줄도 프론트 디버깅용으로 노출 가능
                # "provider": "kakao",
                # "social_id": str(kakao_id),
            }
        }
        return Response(TokenPairResponseSerializer(out).data, status=200)
    
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class AIAuthentication(BaseAuthentication):
    def authenticate(self, request):
        ai_secret = request.headers.get("X-AI-SECRET")

        if not ai_secret or ai_secret != settings.AI_SECRET_KEY:
            raise AuthenticationFailed("AI 인증 실패")

        return (None, None)  # 유저 객체는 필요 없으므로
    
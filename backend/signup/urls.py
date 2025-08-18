from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import KakaoLoginAPIView

urlpatterns = [
    path("auth/kakao/", KakaoLoginAPIView.as_view(), name="kakao-login"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token-obtain"), # 포스트맨에서의 토큰 생성을 위해 임시로
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
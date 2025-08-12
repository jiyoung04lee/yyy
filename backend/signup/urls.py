from django.urls import path
from .views import KakaoLoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("auth/kakao/", KakaoLoginAPIView.as_view(), name="kakao-login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]

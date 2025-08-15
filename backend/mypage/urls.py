from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MypageMainViewSet, ReviewViewSet, ReportViewSet, ExtraSettingViewSet

router = DefaultRouter()
router.register(r'mypage', MypageMainViewSet, basename='mypage')  # 메인 화면
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'extra-settings', ExtraSettingViewSet, basename='extra-setting')

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MypageMainViewSet, ReviewViewSet, ReportViewSet, ExtraSettingViewSet, ProfileUpdateView

router = DefaultRouter()
router.register(r'main', MypageMainViewSet, basename='main')  # 메인 화면
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'extra-settings', ExtraSettingViewSet, basename='extra-setting')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', ProfileUpdateView.as_view(), name='mypage-profile-update'),
]
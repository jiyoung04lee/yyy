from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet, ReportViewSet, ExtraSettingViewSet

# DRF Router 생성
router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'extra-settings', ExtraSettingViewSet, basename='extra-setting')

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartyViewSet, PartyJoinAPIView, PartyLeaveAPIView

app_name = "detailview"

router = DefaultRouter()
router.register(r"parties", PartyViewSet, basename="party")

urlpatterns = [
    path("", include(router.urls)),
    path("parties/<int:party_id>/join/", PartyJoinAPIView.as_view(), name="party-join"),
    path("parties/<int:party_id>/leave/", PartyLeaveAPIView.as_view(), name="party-leave"),  # 선택
]

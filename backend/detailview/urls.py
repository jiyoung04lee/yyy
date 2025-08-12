from django.urls import path
from .views import PartyDetailView, ParticipationCreateView

app_name = "detailview"

urlpatterns = [
    path("parties/<int:pk>/", PartyDetailView.as_view(), name="party-detail"),
    path("parties/<int:pk>/participations/", ParticipationCreateView.as_view(), name="party-join"),
]

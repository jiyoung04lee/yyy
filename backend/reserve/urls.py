from django.urls import path
from .views import JoinAndReserveView

app_name = "reserve"

urlpatterns = [
    path("join/", JoinAndReserveView.as_view(), name="join-and-reserve"),
]
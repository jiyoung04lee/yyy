from django.urls import path
from detailview.views import PartyListForHomeView  # deatailview와 같은 뷰 사용

app_name = "homemap"

urlpatterns = [
    path("home/", PartyListForHomeView.as_view(), name="home-parties"),
    path("map/",  PartyListForHomeView.as_view(), name="map-parties"),
]

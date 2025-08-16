from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/notice/(?P<user_id>\d+)/$", consumers.NoticeConsumer.as_asgi()),
]
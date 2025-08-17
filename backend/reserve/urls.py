from django.urls import path
from .views import CreatePaymentView

app_name = "reserve"

urlpatterns = [
    path("pay/", CreatePaymentView.as_view(), name="create-payment"), # 예약금 결제 처리 기능 API
]

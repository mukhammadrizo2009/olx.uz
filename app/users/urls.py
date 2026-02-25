from django.urls import path
from .views import TelegramLoginView

urlpatterns = [
    path("auth/telegram/", TelegramLoginView.as_view(), name="telegram-login"),
]
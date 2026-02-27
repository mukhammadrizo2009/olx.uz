from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def telegram_login(data: dict):
    """
    Telegram orqali login yoki register qilish
    """

    user, created = User.objects.get_or_create(
        telegram_id=data["telegram_id"],
        defaults={
            "username": data.get("username", ""),
            "first_name": data.get("first_name", ""),
            "last_name": data.get("last_name", ""),
            "role": "customer",
        }
    )

    refresh = RefreshToken.for_user(user)

    return {
        "user": user,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "created": created
    }
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import TelegramAuthSerializer


User = get_user_model()


class TelegramLoginView(APIView):

    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        telegram_id = data["telegram_id"]

        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "username": data.get("username") or f"user_{telegram_id}",
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
                "role": "CUSTOMER",
            }
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)
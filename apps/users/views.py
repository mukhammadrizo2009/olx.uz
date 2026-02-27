from django.contrib.auth import get_user_model

from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import TelegramAuthSerializer
from .services import telegram_login


User = get_user_model()


class TelegramLoginView(APIView):

    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = telegram_login(serializer.validated_data)

        return Response({
            "user_id": result["user"].id,
            "telegram_id": result["user"].telegram_id,
            "role": result["user"].role,
            "access": result["access"],
            "refresh": result["refresh"],
        })
        
        
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "telegram_id": request.user.telegram_id,
            "role": request.user.role
        })
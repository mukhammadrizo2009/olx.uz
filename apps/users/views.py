from django.contrib.auth import get_user_model

from rest_framework import generics, status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import TelegramAuthSerializer, UserProfileSerializer, SellerProfileSerializer
from .services import telegram_login

from .models import SellerProfile

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
    
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Log out qilindi."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid Token."}, status=status.HTTP_400_BAD_REQUEST)

        
class RefreshTokenView(TokenRefreshView):
    pass


class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UpgradeToSellerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role == 'seller':
            return Response({"detail": "Siz allaqachon sotuvchisiz."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.role = 'seller'
        user.save()
        

        SellerProfile.objects.get_or_create(user=user)
        
        return Response({
            "message": "Tabriklaymiz, siz endi sotuvchisiz!",
            "role": user.role
        }, status=status.HTTP_200_OK)


class SellerDetailView(generics.RetrieveAPIView):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    permission_classes = [AllowAny]

class SellerProductsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, seller_id):
        return Response({"message": f"{seller_id} id dagi sotuvchi mahsulotlari ro'yxati"}, status=status.HTTP_200_OK)
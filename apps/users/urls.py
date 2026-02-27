from django.urls import path
from .views import TelegramLoginView, RefreshTokenView, LogoutView, MeView, UpgradeToSellerView, SellerProductsView, SellerDetailView

urlpatterns = [
    path("v1/auth/telegram/", TelegramLoginView.as_view(), name="telegram-login"),
    path('v1/auth/refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('v1/auth/logout/', LogoutView.as_view(), name='logout-user'),
    path('v1/users/me/', MeView.as_view(), name='user-me'),
    path('v1/users/me/upgrade-to-seller/', UpgradeToSellerView.as_view(), name='upgrade-seller'),
    path('v1/sellers/<int:pk>/', SellerDetailView.as_view(), name='seller-detail'),
    path('v1/sellers/<int:user_id>/products/', SellerProductsView.as_view(), name='seller-products'),
]
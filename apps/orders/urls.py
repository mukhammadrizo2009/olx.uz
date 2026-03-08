from django.urls import path
from .views import OrderView, OrderDetailView

urlpatterns = [
    
    path("v1/orders/", OrderView.as_view(), name="orders-list-create"),
    path("v1/orders/<int:pk>/", OrderDetailView.as_view(), name="orders-detail"),
    
]
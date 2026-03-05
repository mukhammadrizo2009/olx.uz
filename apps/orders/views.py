from rest_framework import generics, permissions
from .models import Order
from .serializers import OrderCreateSerializer, OrderStatusUpdateSerializer, OrderDetailSerializer, OrderListSerializer
from .permissions import IsOrderParticipant
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Order"])
class OrderView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = self.request.query_params.get("role")

        if role == "seller":
            return Order.objects.filter(seller=user)
        return Order.objects.filter(buyer=user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderListSerializer
    
    
@extend_schema(tags=["Order"])
class OrderDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOrderParticipant]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return OrderStatusUpdateSerializer
        return OrderDetailSerializer

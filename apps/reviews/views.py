from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Reviews"])
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Fikrni tahrirlash mumkin emas."},
            status=405
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Fikrni tahrirlash mumkin emas."},
            status=405
        )
        
    def get_queryset(self):
        queryset = Review.objects.all()
        seller_id = self.request.query_params.get("seller_id")

        if seller_id:
            queryset = queryset.filter(seller_id=seller_id)

        return queryset
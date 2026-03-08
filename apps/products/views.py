from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from django.db.models import F

from .models import Product
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateSerializer
)
from .permissions import IsSellerOrReadOnly, IsOwner

@extend_schema(tags=["Products"])
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSellerOrReadOnly]
    def get_queryset(self):
        queryset = Product.objects.all().select_related(
            "seller", "category"
        ).prefetch_related("images")

        if self.action == "list":
            return queryset.filter(status=Product.Status.ACTIVE)

        return queryset


    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        elif self.action == "create":
            return ProductCreateSerializer
        return ProductDetailSerializer


    def perform_create(self, serializer):
        serializer.save(
            seller=self.request.user,
            status=Product.Status.MODERATION
        )


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        Product.objects.filter(pk=instance.pk).update(
            view_count=F("view_count") + 1
        )

        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = self.get_object()

        if instance.status == Product.Status.ACTIVE:
            serializer.save(status=Product.Status.MODERATION)
        else:
            serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True, methods=["post"], permission_classes=[IsOwner])
    def publish(self, request, pk=None):
        product = self.get_object()

        product.status = Product.Status.ACTIVE
        product.published_at = timezone.now()
        product.save()

        return Response({"message": "E'lon aktiv qilindi."})

    @action(detail=True, methods=["post"], permission_classes=[IsOwner])
    def archive(self, request, pk=None):
        product = self.get_object()

        product.status = Product.Status.ARCHIVED
        product.save()

        return Response({"message": "E'lon arxivlandi."})

    @action(detail=True, methods=["post"], permission_classes=[IsOwner])
    def sold(self, request, pk=None):
        product = self.get_object()

        product.status = Product.Status.SOLD
        product.save()

        return Response({"message": "E'lon sotilgan deb belgilandi."})
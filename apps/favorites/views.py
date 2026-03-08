from rest_framework import generics, permissions
from .models import Favorite
from .serializers import FavoriteSerializer
from .permissions import IsFavoriteOwner
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Favourites"])
class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()
        
    def get(self, request, *args, **kwargs):
        print("AUTH HEADER:", request.headers.get("Authorization"))
        print("USER:", request.user)
        return super().get(request, *args, **kwargs)


@extend_schema(tags=["Favourites"])
class FavoriteDeleteView(generics.DestroyAPIView):
    
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated, IsFavoriteOwner]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        product = instance.product

        # count kamaytirish
        if product.favourite_count > 0:
            product.favourite_count -= 1
            product.save(update_fields=['favourite_count'])

        instance.delete()
        
   
from rest_framework import generics
from drf_spectacular.utils import extend_schema

from apps.products.models import Product
from apps.products.serializers import ProductListSerializer

from .permissions import IsAdminOrReadOnly
from .models import Category
from .serializers import CategorySerializer


@extend_schema(tags=["Categories"])
class Categories(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(tags=["Categories"])
class OneCategory(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    
    
@extend_schema(tags=["Categories"])
class ActiveProduct(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        return Product.objects.filter(
            category__slug=category_slug,
            status='published'
        )
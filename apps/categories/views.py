from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Category
from .serializers import CategorySerializer
from apps.products.models import Product
from apps.products.serializers import ProductListSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Categories"])
class Categories(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_active=True, parent=None).order_by('order_num')
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]     
       
@extend_schema(tags=["Categories"])
class OneCategory(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]
    
@extend_schema(tags=["Categories"])
class ActiveProduct(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        return Product.objects.filter(
            category__slug=category_slug,
            is_active=True
        )
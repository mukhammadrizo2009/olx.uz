from django.urls import path
from .views import ProductViewSet

urlpatterns = [
    
    path("v1/products/", ProductViewSet.as_view({"get": "list", "post": "create",}), name="product-list"),
    path("v1/products/<int:pk>/", ProductViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy",}), name="product-detail"),
    path("v1/products/<int:pk>/publish/", ProductViewSet.as_view({"post": "publish",}), name="product-publish"),
    path("v1/products/<int:pk>/archive/", ProductViewSet.as_view({"post": "archive",}), name="product-archive"),
    path("v1/products/<int:pk>/sold/", ProductViewSet.as_view({"post": "sold",}), name="product-sold"),
    
]
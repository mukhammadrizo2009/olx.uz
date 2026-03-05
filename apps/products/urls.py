from django.urls import path
from .views import FavoriteDeleteView, FavoriteListCreateView


urlpatterns = [
    path("v1/favorites/", FavoriteListCreateView.as_view()),
    path("v1/favorites/<int:pk>/", FavoriteDeleteView.as_view()),
    #path("v1/products/", ),
    #path("v1/products/{id}/", ),
    #path("v1/products/{id}/", ),
    #path("v1/products/{id}/publish/", ),
    #path("v1/products/{id}/archive/", ),
    #path("v1/products/{id}/sold/", ),
]
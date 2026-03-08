from django.urls import path
from .views import FavoriteDeleteView, FavoriteListCreateView


urlpatterns = [
    
    path("v1/favorites/", FavoriteListCreateView.as_view()),
    path("v1/favorites/<int:pk>/", FavoriteDeleteView.as_view()),
    
    ]
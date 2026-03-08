from django.urls import path
from .views import ReviewViewSet

review_list = ReviewViewSet.as_view({'get': 'list', 'post': 'create',})
review_detail = ReviewViewSet.as_view({'get': 'retrieve',})

urlpatterns = [
    
    path('v1/reviews/', review_list, name='review-list'),
    path('v1/reviews/<int:pk>/', review_detail, name='review-detail'),
]
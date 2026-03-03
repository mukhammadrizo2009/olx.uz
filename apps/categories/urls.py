from django.urls import path
from .views import Categories, OneCategory, ActiveProduct

urlpatterns = [
    path('v1/categories/', Categories.as_view(), name='categories'),
    path('v1/categories/{slug}/', OneCategory.as_view(), name='one-category'),
    path('v1/categories/{slug}/products/', ActiveProduct.as_view(), name='active-product')
]
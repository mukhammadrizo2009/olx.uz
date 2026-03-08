from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, ProductImage
from apps.categories.serializers import CategorySerializer

User = get_user_model()

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            'id',
            'image',
            'order',
            'is_main',
            'created_at'
        ]
        
class ProductListSerializer(serializers.ModelSerializer):

    seller = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'seller',
            'category',
            'title',
            'price',
            'price_type',
            'region',
            'district',
            'view_count',
            'favourite_count',
            'status',
            'images',
            'created_at'
        ]
        
class ProductDetailSerializer(serializers.ModelSerializer):

    seller = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        
class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = [
            'seller',
            'view_count',
            'favourite_count',
            'status',
            'published_at',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['seller'] = user
        return super().create(validated_data)

    def validate(self, data):
        if data.get('price_type') == Product.Price_type.FREE:
            data['price'] = 0
        return data
    
    
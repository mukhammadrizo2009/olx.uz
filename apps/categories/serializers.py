from rest_framework import serializers
from .models import Category

class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'parent',
            'name',
            'slug',
            'children'
        ]
        
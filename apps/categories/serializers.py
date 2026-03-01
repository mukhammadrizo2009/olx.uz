from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'parent',
            'name',
            'slug',
            'icon',
            'description',
            'is_active',
            'order_num',
            'children',
            'created_at'
        ]
        read_only_fields = ['slug']

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []
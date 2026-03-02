from rest_framework import serializers
from apps.orders.models import Order
from apps.products.models import Product


class OrderCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = [
            'id',
            'product',
            'final_price',
            'meeting_location',
            'meeting_time',
            'notes',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        product = attrs.get('product')
        request = self.context.get('request')

        if product.seller == request.user:
            raise serializers.ValidationError("O'zingizning mahsulotingizni sotib olmaysiz.")

        if not attrs.get('final_price'):
            attrs['final_price'] = product.price

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        product = validated_data['product']

        order = Order.objects.create(
            buyer=request.user,
            seller=product.seller,
            **validated_data
        )

        return order
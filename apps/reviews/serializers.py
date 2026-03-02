from rest_framework import serializers
from apps.reviews.models import Review
from apps.orders.models import Order


class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'id',
            'order',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        request = self.context.get('request')
        order = attrs.get('order')

        if order.buyer != request.user:
            raise serializers.ValidationError(
                "Faqat buyurtma beruvchi fikr qoldira oladi."
            )
            
        if order.status != Order.Status.PURCHASED:
            raise serializers.ValidationError(
                "Faqat sotib olingan buyurtmaga fikr qoldirish mumkin."
            )
            
        if hasattr(order, 'review'):
            raise serializers.ValidationError(
                "Bu buyurtmaga allaqachon fikr qoldirilgan."
            )

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        order = validated_data['order']

        review = Review.objects.create(
            reviewer=request.user,
            seller=order.seller,
            **validated_data
        )

        return review
    
class ReviewSerializer(serializers.ModelSerializer):

    reviewer_username = serializers.CharField(
        source='reviewer.username',
        read_only=True
    )

    seller_username = serializers.CharField(
        source='seller.username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
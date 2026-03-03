from rest_framework import serializers
from .models import Order

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
        read_only_fields = ['id', 'created_at', 'final_price']

    def validate(self, attrs):
        request = self.context['request']
        product = attrs['product']

        if product.seller == request.user:
            raise serializers.ValidationError(
                "O'zingizning mahsulotingizni sotib olmaysiz."
            )

        return attrs

    def create(self, validated_data):
        request = self.context['request']
        product = validated_data['product']

        return Order.objects.create(
            buyer=request.user,
            seller=product.seller,
            product=product,
            final_price=product.price,
            **validated_data
        )
        
class OrderStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'status',
            'meeting_location',
            'meeting_time',
            'final_price'
        ]

    def validate(self, attrs):
        request = self.context['request']
        order = self.instance

        user = request.user

        if user != order.seller and user != order.buyer:
            raise serializers.ValidationError("Ruxsat yo'q.")

        new_status = attrs.get('status')

        # Seller rules
        if user == order.seller:
            if order.status != Order.Status.WAITING:
                raise serializers.ValidationError("Seller faqat WAITING holatda o'zgartira oladi.")

            if new_status not in [Order.Status.AGREED, Order.Status.REJECT]:
                raise serializers.ValidationError("Noto'g'ri status.")

        # Buyer rules
        if user == order.buyer:
            if order.status != Order.Status.AGREED:
                raise serializers.ValidationError("Buyer faqat AGREED holatda o'zgartira oladi.")

            if new_status not in [Order.Status.PURCHASED, Order.Status.REJECT]:
                raise serializers.ValidationError("Noto'g'ri status.")

        return attrs

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        # Agar sotib olinsa
        if instance.status == Order.Status.PURCHASED:
            product = instance.product
            product.status = "SOLD"
            product.save()

            seller = instance.seller
            seller.total_sales += 1
            seller.save()

        return instance
    
class OrderListSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_image = serializers.ImageField(source='product.main_image.image', read_only=True)
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'product',
            'product_title',
            'product_image',
            'buyer_username',
            'seller_username',
            'final_price',
            'status',
            'created_at',
        ]
        
class OrderDetailSerializer(serializers.ModelSerializer):

    product = serializers.SerializerMethodField()
    buyer = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'product',
            'buyer',
            'seller',
            'final_price',
            'status',
            'meeting_location',
            'meeting_time',
            'notes',
            'created_at',
            'updated_at',
        ]

    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "title": obj.product.title,
            "price": obj.product.price,
            "status": obj.product.status,
        }

    def get_buyer(self, obj):
        return {
            "id": obj.buyer.id,
            "username": obj.buyer.username,
        }

    def get_seller(self, obj):
        return {
            "id": obj.seller.id,
            "username": obj.seller.username,
        }
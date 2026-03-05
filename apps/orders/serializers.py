from rest_framework import serializers
from .models import Order

class OrderCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    notes = serializers.CharField(required=False)

    def create(self, validated_data):
        from apps.products.models import Product
        from apps.orders.order_service import OrderService

        product = Product.objects.get(id=validated_data["product_id"])
        buyer = self.context["request"].user

        return OrderService.create_order(
            product=product,
            buyer=buyer,
            notes=validated_data.get("notes", "")
        )
        
class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)
    meeting_location = serializers.CharField(required=False)
    meeting_time = serializers.DateTimeField(required=False)
    final_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)

    def update(self, instance, validated_data):
        from apps.orders.order_service import OrderService

        return OrderService.change_status(
            order=instance,
            user=self.context["request"].user,
            new_status = validated_data.get("status"),
            data=validated_data
        )
    
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
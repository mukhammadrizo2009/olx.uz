from rest_framework import serializers
from rest_framework import serializers
from .models import User, SellerProfile


class TelegramAuthSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'telegram_id', 'username', 'first_name', 'last_name', 'phone_number', 'role']
        read_only_fields = ['id', 'telegram_id', 'role']

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = '__all__'


class SellerProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = SellerProfile
        fields = [
            'user', 'username', 'shop_name', 'shop_description', 
            'shop_logo', 'region', 'district', 'address', 
            'rating', 'total_sales', 'created_at'
        ]
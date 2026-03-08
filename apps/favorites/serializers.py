from rest_framework import serializers
from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ['id', 'product', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']

        favorite, created = Favorite.objects.get_or_create(
            user=user,
            product=product
        )

        if created:
            product.favourite_count += 1
            product.save(update_fields=['favourite_count'])

        return favorite
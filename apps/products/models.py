from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from apps.categories.models import Category

User = get_user_model()

class Product(models.Model):
    
    def default_expiry():
        return timezone.now() + timedelta(days=30)
    
    class Role(models.TextChoices):
        NEW = "NEW", "Yangi"
        PERFECT = "PERFECT", "Ideal"
        GOOD = "GOOD", "Yahshi"
        NOT_BAD = "NOT_BAD", "Qoniqarli"
    
    class Price_type(models.TextChoices):
        STRICT = "STRICT", "Qat'iy"
        AGREED = 'AGREED', "Kelishiladi"
        FREE = "FREE", "Bepul"
        EXCHANGE = "EXCHANGE", "Ayirboshlash"
    
    class Status(models.TextChoices):
        MODERATION = "MODERATION", "Moderatsida"
        ACTIVE = "ACTIVE", "Aktiv"
        REJECT = "REJECT", "Rad etilgan"
        SOLD = "SOLD", "Sotilgan"
        ARCHIVED = "ARCHIVED", "Arxivlangan"
        
    

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    conditions = models.CharField(
        max_length=10,
        choices=Role,
        default=Role.NEW
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
        )
    price_type = models.CharField(
        max_length=10,
        choices=Price_type,
        default=Price_type.AGREED
        )
    region = models.CharField(max_length=150, null=False)
    district = models.CharField(max_length=150, null=False)
    view_count = models.PositiveIntegerField(default=0)
    favourite_count = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=10,
        choices=Status,
        default=Status.MODERATION
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True)

    expires_at = models.DateTimeField(default=default_expiry)
    


class ProductImage(models.Model):

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='products/')
    order = models.PositiveIntegerField(default=0)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(
                product=self.product,
                is_main=True
            ).update(is_main=False)
        super().save(*args, **kwargs)


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'product'),)
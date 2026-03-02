from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product

User = get_user_model()

class Order(models.Model):
    
    class Status(models.TextChoices):
        WAITING = "WAITING", "Kutilyabdi"
        AGREED = "AGREED", "Kelishilgan"
        PURCHASED = "PURCHASED", "Sotib olingan"
        REJECT = "REJECT", "Bekor qilingan"
        
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyer_orders'
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='seller_orders'
    )
    final_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=Status,
        default=Status.WAITING
        )
    meeting_location = models.CharField(max_length=250, blank=True)
    meeting_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.final_price:
            self.final_price = self.product.price

        if not self.seller:
            self.seller = self.product.seller

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} | {self.buyer}"
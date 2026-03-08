from django.db import models
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.orders.models import Order

User = get_user_model()

class Review(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='review'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        if not self.seller:
            self.seller = self.order.seller

        super().save(*args, **kwargs)

        avg_rating = Review.objects.filter(
            seller=self.seller
        ).aggregate(avg=Avg("rating"))["avg"] or 0

        self.seller.rating = round(avg_rating, 2)
        self.seller.save(update_fields=["rating"])
            
        def __str__(self):
            return f"{self.order} | {self.rating}"
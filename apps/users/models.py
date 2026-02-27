from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Xaridor"
        SELLER = "SELLER", "Sotuvchi"

    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    phone_number = models.CharField(
        max_length=13,
        blank=True,
    )
    role = models.CharField(
        max_length=8,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} | {self.role}"

class SellerProfile(models.Model):
    
    Auth_User = settings.AUTH_USER_MODEL
    user = models.OneToOneField(
        Auth_User, 
        on_delete=models.CASCADE, 
        primary_key=True, 
        related_name='seller_profile'
    )
    
    shop_name = models.CharField(max_length=255, unique=True)
    shop_description = models.TextField(blank=True, null=True)
    shop_logo = models.ImageField(upload_to='sellers/logos/', blank=True, null=True)
    
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    
    rating = models.FloatField(default=0)
    total_sales = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop_name

    class Meta:
        verbose_name = "Seler Profile"
        verbose_name_plural = "Sellers Profile"